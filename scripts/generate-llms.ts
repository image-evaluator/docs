import fs from 'node:fs';
import path from 'node:path';

interface Frontmatter {
  title: string;
  description: string;
  body: string;
}

interface MetaConfig {
  title: string;
  pages: string[];
}

interface PageData {
  slug: string;
  title: string;
  description: string;
  rawContent: string;
  cleanedBody: string;
}

const EMOJI_REGEX = /[\u{1F300}-\u{1F9FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}\u{1F100}-\u{1F1FF}\u{1F200}-\u{1F2FF}\u{1F600}-\u{1F64F}\u{1F680}-\u{1F6FF}\u{1FA70}-\u{1FAFF}\u{2300}-\u{23FF}\u{2B50}\u{200D}\u{FE0F}]/gu;

function parseFrontmatter(rawContent: string): Frontmatter {
  const match = rawContent.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/);
  if (!match) {
    return { title: '', description: '', body: rawContent };
  }
  const fmBlock: string = match[1];
  const body: string = match[2];
  let title = '';
  let description = '';
  for (const line of fmBlock.split('\n')) {
    const trimmed: string = line.trim();
    if (trimmed.startsWith('title:')) {
      title = trimmed.slice(6).trim().replace(/^['"]|['"]$/g, '');
    } else if (trimmed.startsWith('description:')) {
      description = trimmed.slice(12).trim().replace(/^['"]|['"]$/g, '');
    }
  }
  return { title, description, body };
}

function extractMetricTable(indexMdxContent: string): string {
  const match = indexMdxContent.match(/(\| 评估维度 \|[\s\S]*?\n(?!\s*\|))/);
  if (match) {
    return match[1].trim();
  }
  return '';
}

function cleanMdxToMarkdown(body: string, title: string): string {
  let content: string = body.trimStart();

  // Strip duplicate H1 matching title at start of body
  const escapedTitle: string = title.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  content = content.replace(new RegExp(`^#\\s*${escapedTitle}\\s*\\n+`), '');

  // Replace Accordion tags
  content = content.replace(/<Accordion\s+title="([^"]+)">([\s\S]*?)<\/Accordion>/g, (_: string, accordionTitle: string, inner: string): string => {
    const lines: string[] = inner.split('\n');
    const dedentedLines: string[] = lines.map((line: string): string => line.replace(/^[ ]{1,4}/, ''));
    return `\n\n### ${accordionTitle}\n\n${dedentedLines.join('\n').trim()}\n\n`;
  });

  // Handle any remaining Accordion / Accordions tags
  content = content.replace(/<\/?Accordions>/g, '');
  content = content.replace(/<Accordion\s+title="([^"]+)">/g, '### $1\n\n');
  content = content.replace(/<\/Accordion>/g, '');

  // Replace Step / Steps tags
  content = content.replace(/<Step>([\s\S]*?)<\/Step>/g, (_: string, inner: string): string => {
    const lines: string[] = inner.split('\n');
    const dedentedLines: string[] = lines.map((line: string): string => line.replace(/^[ ]{1,4}/, ''));
    return `\n\n${dedentedLines.join('\n').trim()}\n\n`;
  });
  content = content.replace(/<\/?Steps>/g, '');
  content = content.replace(/<\/?Step>/g, '');

  // Replace custom visual components
  content = content.replace(/<ImageComparison[\s\S]*?(?:\/>|<\/ImageComparison>)/g, '> [交互组件说明: 参见网页版双图对比滑块]');
  content = content.replace(/<MetricVisualShowcase[\s\S]*?(?:\/>|<\/MetricVisualShowcase>)/g, '> [交互组件说明: 参见网页版视觉评测用例演练]');

  // Remove or sanitize any other JSX/HTML self-closing or paired tags cleanly (excluding math / markdown brackets)
  content = content.replace(/<\/?[A-Z][a-zA-Z0-9]*(?:\s+[^>]*)?\/?>/g, '');

  // Trim leading whitespace on headings
  content = content.replace(/^[ \t]+(#{1,6}\s)/gm, '$1');

  // Strip lines that only contain whitespace
  content = content.replace(/^[ \t]+$/gm, '');

  // Normalize excessive blank lines
  content = content.replace(/\n{3,}/g, '\n\n');

  return content.trim();
}

function ensureBlankLineBeforeCodeBlockEnd(content: string): string {
  const lines: string[] = content.split('\n');
  const result: string[] = [];
  let inCodeBlock = false;
  let codeFence = '';

  for (let i = 0; i < lines.length; i++) {
    const line: string = lines[i];
    const fenceMatch = line.match(/^(\s*)(`{3,}|~{3,})/);

    if (!inCodeBlock) {
      if (fenceMatch) {
        inCodeBlock = true;
        codeFence = fenceMatch[2];
      }
      result.push(line);
    } else {
      const isClosing: boolean = line.trim() === codeFence;
      if (isClosing) {
        const prevLine: string = result.length > 0 ? result[result.length - 1] : '';
        if (prevLine.trim() !== '') {
          result.push('');
        } else {
          result[result.length - 1] = '';
        }
        inCodeBlock = false;
        codeFence = '';
      }
      result.push(line);
    }
  }

  return result.join('\n');
}

function removeEmojis(text: string): string {
  return text.replace(EMOJI_REGEX, '');
}

async function main(): Promise<void> {
  const currentDir: string = process.cwd();
  const docsSiteDir: string = fs.existsSync(path.join(currentDir, 'content/docs/meta.json'))
    ? currentDir
    : path.join(currentDir, 'docs-site');

  const contentDocsDir: string = path.join(docsSiteDir, 'content/docs');
  const publicDir: string = path.join(docsSiteDir, 'public');
  const metaPath: string = path.join(contentDocsDir, 'meta.json');

  if (!fs.existsSync(metaPath)) {
    throw new Error(`meta.json not found at ${metaPath}`);
  }

  if (!fs.existsSync(publicDir)) {
    fs.mkdirSync(publicDir, { recursive: true });
  }

  const metaContent: string = fs.readFileSync(metaPath, 'utf-8');
  const meta: MetaConfig = JSON.parse(metaContent);

  const pagesData: PageData[] = [];

  for (const slug of meta.pages) {
    const mdxPath: string = path.join(contentDocsDir, `${slug}.mdx`);
    if (!fs.existsSync(mdxPath)) {
      console.warn(`Warning: MDX file not found for slug: ${slug} at ${mdxPath}`);
      continue;
    }
    const rawContent: string = fs.readFileSync(mdxPath, 'utf-8');
    const { title, description, body } = parseFrontmatter(rawContent);
    const cleanedBody: string = cleanMdxToMarkdown(body, title);
    pagesData.push({ slug, title, description, rawContent, cleanedBody });
  }

  // 1. Generate llms.txt
  const indexPage: PageData | undefined = pagesData.find((p: PageData): boolean => p.slug === 'index');
  const metricTable: string = indexPage ? extractMetricTable(indexPage.rawContent) : '';

  const indexList: string = pagesData
    .map((p: PageData): string => `- [${p.title}](/docs${p.slug === 'index' ? '' : '/' + p.slug}): ${p.description}`)
    .join('\n');

  const cliSection: string = [
    '```bash',
    '# 1. 单图视觉美学评分',
    'image-evaluator --metrics aesthetic --image path/to/sample.png',
    '',
    '# 2. 图文对齐与人类偏好评分',
    'image-evaluator --metrics clip pickscore \\',
    '    --image path/to/sample.png \\',
    '    --prompt "a photograph of an astronaut riding a horse on mars"',
    '',
    '# 3. 成对图像保真度评估 (LPIPS, SSIM, PSNR)',
    'image-evaluator --metrics lpips ssim psnr \\',
    '    --image path/to/generated.png \\',
    '    --reference path/to/reference.png',
    '',
    '# 4. 数据集分布距离评测 (FID, KID)',
    'image-evaluator --metrics fid kid \\',
    '    --image path/to/generated_folder/ \\',
    '    --reference path/to/real_folder/',
    '',
    '```',
  ].join('\n');

  const llmsTxtContent: string = [
    '# Image Evaluator',
    '> 生产级多维图像生成评测工具库，覆盖美学质量、语义对齐、主体保真、成对失真、分布差异与人类偏好 9 大核心评测指标。',
    '',
    '## 文档索引',
    indexList,
    '',
    '## 核心指标矩阵',
    metricTable,
    '',
    '## 命令行使用范例',
    cliSection,
    '',
    '## 全量技术文档',
    '- [全量文档纯文本 (LLMs Full)](/llms-full.txt): 专为 512K 级上下文大语言模型设计的完整技术参考与诊断指南。',
    '',
  ].join('\n');

  const finalLlmsTxt: string = removeEmojis(ensureBlankLineBeforeCodeBlockEnd(llmsTxtContent));
  const llmsTxtPath: string = path.join(publicDir, 'llms.txt');
  fs.writeFileSync(llmsTxtPath, finalLlmsTxt, 'utf-8');
  console.log(`Generated: ${llmsTxtPath} (${Buffer.byteLength(finalLlmsTxt, 'utf-8')} bytes)`);

  // 2. Generate llms-full.txt
  const fullHeader: string = [
    '# Image Evaluator 全量技术文档 (LLMs Full)',
    '> 本文档汇集 Image Evaluator 9 大评测指标的全部权威说明、理论推导、API 规范、CLI 用法、边界陷阱与诊断建议，专为 512K 大模型机读与上下文注入设计。',
  ].join('\n');

  const pageSections: string[] = pagesData.map((p: PageData): string => {
    return `# ${p.title}\n\n> ${p.description}\n\n${p.cleanedBody}`;
  });

  const fullContentRaw: string = [fullHeader, ...pageSections].join('\n\n---\n\n') + '\n';
  const finalLlmsFull: string = removeEmojis(ensureBlankLineBeforeCodeBlockEnd(fullContentRaw));
  const llmsFullPath: string = path.join(publicDir, 'llms-full.txt');
  fs.writeFileSync(llmsFullPath, finalLlmsFull, 'utf-8');
  console.log(`Generated: ${llmsFullPath} (${Buffer.byteLength(finalLlmsFull, 'utf-8')} bytes)`);
}

main().catch((err: unknown) => {
  console.error('Error generating llms files:', err);
  process.exit(1);
});
