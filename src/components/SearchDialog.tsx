'use client';

import React, { useState, useRef, useEffect, useCallback, useMemo } from 'react';
import { useRouter } from 'next/navigation';
import {
  SearchDialog,
  SearchDialogClose,
  SearchDialogContent,
  SearchDialogFooter,
  SearchDialogHeader,
  SearchDialogIcon,
  SearchDialogInput,
  SearchDialogList,
  SearchDialogOverlay,
  type SearchItemType,
} from 'fumadocs-ui/components/dialog/search';
import { Sparkles, ArrowLeft, Terminal, BookOpen } from 'lucide-react';

interface SharedProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

interface DocMetric {
  id: string;
  title: string;
  category: string;
  url: string;
  description: string;
  keywords: string[];
}

const DOC_METRICS: DocMetric[] = [
  {
    id: 'lpips',
    title: 'LPIPS (深度感知距离)',
    category: '成对保真度三元组',
    url: '/pairwise/lpips',
    description: 'AlexNet 多尺度深层卷积特征加权感知距离，贴合人类真实视觉判断。',
    keywords: ['lpips', '感知', 'alexnet', '成对', '特征', '距离'],
  },
  {
    id: 'ssim',
    title: 'SSIM (结构相似性)',
    category: '成对保真度三元组',
    url: '/pairwise/ssim',
    description: '局部高斯滑动窗口亮度、对比度与结构三分量统计相似度。',
    keywords: ['ssim', '结构', '相似性', '高斯', '窗口'],
  },
  {
    id: 'psnr',
    title: 'PSNR (峰值信噪比)',
    category: '成对保真度三元组',
    url: '/pairwise/psnr',
    description: '逐像素均方误差对数尺度的底层物理级信号能量重构保真度。',
    keywords: ['psnr', '信噪比', '像素', 'mse', '重构'],
  },
  {
    id: 'fid',
    title: 'FID (弗雷歇感知距离)',
    category: '数据集生成分布',
    url: '/distribution/fid',
    description: 'Inception-v3 特征空间高斯分布协方差二次型距离度量。',
    keywords: ['fid', '弗雷歇', 'inception', '分布', '群体'],
  },
  {
    id: 'kid',
    title: 'KID (核最大均值差异)',
    category: '数据集生成分布',
    url: '/distribution/kid',
    description: '多项式核最大均值差异无偏 U 统计量，专精小样本分布评估。',
    keywords: ['kid', '核', 'mmd', '小样本', '无偏'],
  },
  {
    id: 'aesthetic',
    title: 'Aesthetic (单图美学评分)',
    category: '单图与跨模态对齐',
    url: '/single-image/aesthetic',
    description: '基于 OpenCLIP ViT-L-14 与 MLP 预测人类视觉审美评分。',
    keywords: ['aesthetic', '美学', '打分', 'openclip', '单图'],
  },
  {
    id: 'clip',
    title: 'CLIP Score (图文语义对齐)',
    category: '单图与跨模态对齐',
    url: '/single-image/clip',
    description: '多模态嵌入空间图文余弦相似度客观评测。',
    keywords: ['clip', '图文', '语义', 'prompt', '提示词', '对齐'],
  },
  {
    id: 'arcface',
    title: 'ArcFace (主体身份保真)',
    category: '单图与跨模态对齐',
    url: '/single-image/arcface',
    description: 'InsightFace 512 维特征余弦距离，度量人脸与主体身份一致性。',
    keywords: ['arcface', '人脸', '身份', '一致性', 'insightface'],
  },
  {
    id: 'pickscore',
    title: 'PickScore (真实偏好对齐)',
    category: '人类主观偏好',
    url: '/preference/pickscore',
    description: '基于真实人类成对偏好反馈微调的生成质量打分模型。',
    keywords: ['pickscore', '人类偏好', '偏好', '微调', 'pick-a-pic'],
  },
  {
    id: 'visual-demo',
    title: 'Visual Benchmark (实测演练)',
    category: '交互实测演练',
    url: '/benchmark/visual-demo',
    description: '交互式多维指标看板与双图滑动比对用例演练。',
    keywords: ['visual', 'demo', '演练', '对比', '看板'],
  },
  {
    id: 'overview',
    title: '概览与快速开始',
    category: '文档中心',
    url: '/',
    description: '统一图像质量与多维对齐评估套件完整综述与 CLI 快速指引。',
    keywords: ['index', '概览', '快速开始', '安装', 'cli'],
  },
];

const PRESET_QUERIES = [
  '人脸一致性评测选型建议',
  '全局色偏下 PSNR 暴跌与 LPIPS 机理',
  '小样本生成分布评估 FID vs KID',
];

function getTechnicalAnswer(query: string): string {
  const q = query.toLowerCase();

  if (q.includes('人脸') || q.includes('一致性') || q.includes('arcface') || q.includes('face') || q.includes('身份')) {
    return `### 人脸一致性评测选型建议

1. **核心推荐指标: \`arcface\`**
- 原理机制: 基于 InsightFace buffalo_l 模型提取人脸 512 维归一化深度特征，计算待测图与参考图人脸向量的余弦距离。
- 取值范围与判定: 取值范围为 [0, 2]，数值越小代表身份越一致。通常以 0.40 - 0.50 作为同人判决阈值；余弦距离小于 0.40 表明高度一致。

2. **互补感知评估: \`lpips\` (局部人脸裁剪)**
- 若除身份高层特征外，还需评估面部微观纹理、局部几何拉伸与表情保真度，建议裁剪人脸区域并使用 \`lpips\` 辅助评估。

3. **CLI 快速复现命令:**
\`\`\`bash
image-evaluator --metrics arcface --image generated_face.png --reference real_face.png

\`\`\``;
  }

  if (q.includes('色偏') || q.includes('psnr') || q.includes('lpips') || q.includes('暴跌') || q.includes('像素')) {
    return `### 全局色偏下 PSNR 暴跌与 LPIPS 保持良好的数学机理

1. **PSNR (峰值信噪比) 机制与缺陷:**
- 计算公式: $\\text{PSNR} = 10 \\cdot \\log_{10}(\\frac{\\text{MAX}^2}{\\text{MSE}})$，完全基于逐像素均方误差。
- 暴跌原因: 当图像出现全局轻微色彩偏移（如色调微调）或微小位移时，全图所有像素均产生固定残差，MSE 在整幅图像累积放大，导致对数空间内的 PSNR 出现断崖式暴跌。

2. **LPIPS (深度感知特征相似度) 鲁棒性:**
- 计算机制: LPIPS 在 AlexNet 的多层归一化激活特征空间中计算感知距离。
- 鲁棒原因: 深度卷积特征关注结构轮廓、纹理分布和语义拓扑，对全局常量亮度与色彩平移具有天然的不变性与鲁棒性，贴合人类真实视觉感知。

3. **指标选型指南:**
- 评估生成图像的主观视觉质量时，以 \`lpips\` 为主判定指标；\`psnr\` 仅用于底层严格无损压缩或去噪重构基准。`;
  }

  if (q.includes('小样本') || q.includes('kid') || q.includes('fid') || q.includes('分布') || q.includes('样本量')) {
    return `### 小样本生成分布评估指标选型: FID vs KID

1. **推荐结论: 优先使用 \`kid\` (Kernel Inception Distance)**

2. **核心数学机理与差异:**
- **FID 缺陷**: FID 依赖经验协方差矩阵和均值向量的高斯拟合。在样本量不足（如 $N < 2048$ 甚至几百张）时，存在显著的正向经验估计偏差 (Empirical Bias)，导致计算出的 FID 显著虚高且方差极大。
- **KID 优势**: KID 采用多项式核的最大均值差异 (MMD) 无偏 U 统计量。无论样本规模大小，其期望值均严格无偏，并采用千张子集多次重采样计算均值和标准差，评测结果高度可信。

3. **CLI 快速复现命令:**
\`\`\`bash
image-evaluator --metrics kid --image generated_folder/ --reference real_folder/

\`\`\``;
  }

  if (q.includes('aesthetic') || q.includes('美学') || q.includes('单图')) {
    return `### 单图美学质量评估 (Aesthetic)

- **核心机制**: 基于 OpenCLIP ViT-L-14 归一化多模态特征，接轻量级线性回归头预测人类美学评分。
- **取值范围**: 约 1 到 10 分，数值越高代表视觉美学质量越优。
- **适用场景**: 无参考图生成图像筛选、生成多样性过滤与高质量图库排序。
- **CLI 复现命令:**
\`\`\`bash
image-evaluator --metrics aesthetic --image sample.png

\`\`\``;
  }

  if (q.includes('clip') || q.includes('文本') || q.includes('语义') || q.includes('prompt') || q.includes('对齐')) {
    return `### 图文语义匹配度评估 (CLIP Score)

- **核心机制**: 基于 OpenAI clip-vit-base-patch32 模型，分别提取提示词与生成图像的归一化特征，计算余弦相似度。
- **取值范围**: [0, 1]，数值越高代表图像与文本提示词的语义吻合度越高。
- **CLI 复现命令:**
\`\`\`bash
image-evaluator --metrics clip --image sample.png --prompt "an astronaut on mars"

\`\`\``;
  }

  if (q.includes('pickscore') || q.includes('人类偏好') || q.includes('偏好')) {
    return `### 人类主观偏好评估 (PickScore)

- **核心机制**: 基于真实人类选择数据集 (Pick-a-Pic) 大规模微调的 CLIP ViT-H-14 视觉模型。
- **核心优势**: 相比标准 CLIP 仅判断语义覆盖，PickScore 深入捕获人类审美直觉、负面伪影敏感度与构图完整性。
- **CLI 复现命令:**
\`\`\`bash
image-evaluator --metrics pickscore --image sample.png --prompt "prompt text"

\`\`\``;
  }

  return `### Image Evaluator 评测指标速查

1. **感知视觉质量**: \`aesthetic\` (OpenCLIP ViT-L-14 特征回归，数值越高越优)
2. **图文语义对齐**: \`clip\` (文本与图像余弦相似度), \`pickscore\` (人类主观偏好微调模型)
3. **主体身份一致**: \`arcface\` (InsightFace buffalo_l 512 维余弦距离，< 0.50 同人)
4. **成对保真度**: \`lpips\` (深度感知距离，越低越好), \`ssim\` (结构相似度), \`psnr\` (像素信噪比)
5. **数据集分布**: \`fid\` (大样本高斯距离，N >= 2048), \`kid\` (小样本无偏核多项式距离)

多指标 CLI 联合复现命令:
\`\`\`bash
# 成对全维度对比
image-evaluator --metrics lpips ssim psnr --image gen.png --reference ref.png

# 数据集分布全量评测
image-evaluator --metrics fid kid --image gen_folder/ --reference real_folder/

\`\`\``;
}

export function CustomSearchDialog({ open, onOpenChange }: SharedProps) {
  const [search, setSearch] = useState('');
  const [aiQuery, setAiQuery] = useState<string | null>(null);
  const [aiAnswer, setAiAnswer] = useState<string>('');
  const [isAiLoading, setIsAiLoading] = useState(false);
  const abortControllerRef = useRef<AbortController | null>(null);
  const router = useRouter();

  // Reset state on modal close
  useEffect(() => {
    if (!open) {
      setSearch('');
      setAiQuery(null);
      setAiAnswer('');
      setIsAiLoading(false);
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
    }
  }, [open]);

  const handleAskAI = useCallback(async (queryText: string) => {
    const trimmed = queryText.trim();
    if (!trimmed) return;

    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    const abortController = new AbortController();
    abortControllerRef.current = abortController;

    setAiQuery(trimmed);
    setAiAnswer('');
    setIsAiLoading(true);

    const workerUrl = process.env.NEXT_PUBLIC_AI_WORKER_URL;

    if (workerUrl && workerUrl.trim() !== '') {
      try {
        const endpoint = workerUrl.replace(/\/+$/, '') + '/chat';
        const response = await fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            messages: [{ role: 'user', content: trimmed }],
            stream: true,
          }),
          signal: abortController.signal,
        });

        if (!response.ok || !response.body) {
          throw new Error(`Worker HTTP status ${response.status}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder('utf-8');
        let accumulated = '';
        let doneReading = false;
        let buffer = '';

        while (!doneReading) {
          const { value, done } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split('\n');
          buffer = lines.pop() || '';

          for (const line of lines) {
            const trimmedLine = line.trim();
            if (!trimmedLine || trimmedLine.startsWith(':')) continue;
            if (trimmedLine === 'data: [DONE]') {
              doneReading = true;
              break;
            }
            if (trimmedLine.startsWith('data: ')) {
              try {
                const parsed = JSON.parse(trimmedLine.slice(6));
                const delta =
                  parsed.choices?.[0]?.delta?.content ||
                  parsed.choices?.[0]?.message?.content ||
                  parsed.response ||
                  '';
                if (delta) {
                  accumulated += delta;
                  setAiAnswer(accumulated);
                }
              } catch {
                // Ignore parse errors on SSE frames
              }
            }
          }
        }

        setIsAiLoading(false);
        return;
      } catch {
        if (abortController.signal.aborted) {
          setIsAiLoading(false);
          return;
        }
      }
    }

    // Instant local fallback
    const answer = getTechnicalAnswer(trimmed);
    setAiAnswer(answer);
    setIsAiLoading(false);
  }, []);

  const searchItems: SearchItemType[] = useMemo(() => {
    const q = search.trim().toLowerCase();
    const list: SearchItemType[] = [];

    // AI Trigger Action when user types a query
    if (q.length > 0) {
      list.push({
        id: `ask-ai-${q}`,
        type: 'action',
        node: (
          <div className="flex items-center gap-2 text-fd-primary font-medium">
            <Sparkles className="h-4 w-4 shrink-0 text-fd-primary" />
            <span>智能问答: &ldquo;{search.trim()}&rdquo;</span>
          </div>
        ),
        onSelect: () => {
          void handleAskAI(search.trim());
        },
      });
    }

    // Filter documentation metrics
    const matched = DOC_METRICS.filter((m) => {
      if (!q) return true;
      return (
        m.title.toLowerCase().includes(q) ||
        m.description.toLowerCase().includes(q) ||
        m.keywords.some((k) => k.includes(q))
      );
    });

    for (const m of matched) {
      list.push({
        id: m.id,
        type: 'page',
        url: m.url,
        content: (
          <div className="flex flex-col py-1">
            <div className="flex items-center justify-between text-xs text-fd-muted-foreground mb-0.5">
              <span>{m.category}</span>
            </div>
            <div className="font-semibold text-fd-foreground">{m.title}</div>
            <div className="text-xs text-fd-muted-foreground mt-0.5 leading-normal">
              {m.description}
            </div>
          </div>
        ),
      });
    }

    return list;
  }, [search, handleAskAI]);

  return (
    <SearchDialog
      open={open}
      onOpenChange={onOpenChange}
      search={search}
      onSearchChange={(v) => {
        setSearch(v);
        if (aiQuery) {
          setAiQuery(null);
        }
      }}
      isLoading={isAiLoading}
    >
      <SearchDialogOverlay />
      <SearchDialogContent className="max-w-2xl">
        <SearchDialogHeader>
          <SearchDialogIcon />
          <SearchDialogInput
            placeholder="搜索评测指标或输入技术疑问..."
            onKeyDown={(e) => {
              if (e.key === 'Enter' && search.trim() && !aiQuery) {
                e.preventDefault();
                void handleAskAI(search.trim());
              }
            }}
          />
          <SearchDialogClose />
        </SearchDialogHeader>

        {aiQuery ? (
          <div className="flex flex-col max-h-[60vh] overflow-hidden">
            <div className="flex items-center justify-between border-b border-fd-border bg-fd-secondary/30 px-4 py-2 text-xs">
              <div className="flex items-center gap-2 font-medium text-fd-foreground">
                <Sparkles className="h-3.5 w-3.5 text-fd-primary" />
                <span>技术问答: {aiQuery}</span>
              </div>
              <button
                type="button"
                onClick={() => {
                  setAiQuery(null);
                  setAiAnswer('');
                }}
                className="flex items-center gap-1 rounded px-2 py-1 text-fd-muted-foreground hover:bg-fd-accent hover:text-fd-foreground transition-colors"
              >
                <ArrowLeft className="h-3 w-3" />
                <span>返回文档列表</span>
              </button>
            </div>

            <div className="overflow-y-auto p-4 text-xs sm:text-sm leading-relaxed text-fd-foreground font-sans space-y-3">
              {isAiLoading && !aiAnswer ? (
                <div className="flex items-center gap-2 py-6 text-fd-muted-foreground justify-center">
                  <span className="h-2 w-2 animate-ping rounded-full bg-fd-primary" />
                  <span>正在检索技术知识库...</span>
                </div>
              ) : (
                <div className="whitespace-pre-wrap font-sans text-fd-foreground prose dark:prose-invert max-w-none">
                  {aiAnswer}
                </div>
              )}
            </div>
          </div>
        ) : (
          <SearchDialogList items={searchItems} />
        )}

        <SearchDialogFooter>
          <div className="flex flex-col gap-2 w-full">
            <div className="flex items-center gap-1.5 text-[11px] font-medium text-fd-muted-foreground">
              <Terminal className="h-3 w-3" />
              <span>推荐问题速查:</span>
            </div>
            <div className="flex flex-wrap gap-1.5">
              {PRESET_QUERIES.map((q) => (
                <button
                  key={q}
                  type="button"
                  onClick={() => {
                    setSearch(q);
                    void handleAskAI(q);
                  }}
                  className="rounded border border-fd-border bg-fd-secondary/50 px-2 py-1 text-[11px] text-fd-muted-foreground hover:border-fd-primary hover:text-fd-primary transition-colors"
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        </SearchDialogFooter>
      </SearchDialogContent>
    </SearchDialog>
  );
}

