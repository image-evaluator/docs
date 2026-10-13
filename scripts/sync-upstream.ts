import fs from 'node:fs';
import path from 'node:path';

const REPO_ROOT = path.resolve(import.meta.dirname, '..');
const LOCAL_CHANGELOG_PATH = path.resolve(REPO_ROOT, '../CHANGELOG.md');
const UPSTREAM_RAW_URL =
  'https://raw.githubusercontent.com/neverbiasu/image-evaluator/master/CHANGELOG.md';

const DOCS_EN_PATH = path.resolve(REPO_ROOT, 'content/docs/changelog.mdx');
const DOCS_ZH_PATH = path.resolve(REPO_ROOT, 'content/docs/changelog.zh.mdx');

async function fetchOrReadChangelog(): Promise<string> {
  if (fs.existsSync(LOCAL_CHANGELOG_PATH)) {
    console.log(`Reading local CHANGELOG from: ${LOCAL_CHANGELOG_PATH}`);
    return fs.readFileSync(LOCAL_CHANGELOG_PATH, 'utf-8');
  }

  console.log(`Fetching upstream CHANGELOG from: ${UPSTREAM_RAW_URL}`);
  const res = await fetch(UPSTREAM_RAW_URL);
  if (!res.ok) {
    throw new Error(`Failed to fetch upstream CHANGELOG: HTTP ${res.status}`);
  }
  return await res.text();
}

function sanitizeMdx(content: string): string {
  // Escape unescaped '<' followed by digits (e.g. <20ms) which breaks MDX parser as an unclosed JSX tag
  return content.replace(/<(?=\d)/g, '&lt;');
}

function generateEnglishMdx(rawChangelog: string): string {
  // Strip top # Changelog heading and intros
  const body = sanitizeMdx(
    rawChangelog
      .replace(/^#\s+Changelog\r?\n+/, '')
      .replace(/^All notable[^\n]*\r?\n+/, '')
      .trim()
  );

  return `---
title: Release Notes & Changelog
description: Complete release history and notable changes for image-evaluator
---

# Release Notes & Changelog

All notable user-facing changes to \`image-evaluator\` are documented here.

---

${body}
`;
}

function generateChineseMdx(rawChangelog: string): string {
  let body = sanitizeMdx(
    rawChangelog
      .replace(/^#\s+Changelog\r?\n+/, '')
      .replace(/^All notable[^\n]*\r?\n+/, '')
      .trim()
  );

  // Localize standard section headers
  body = body
    .replace(/^###\s+Changed\s*$/gm, '### 变更项')
    .replace(/^###\s+Fixed\s*$/gm, '### 修复项')
    .replace(/^###\s+Added\s*$/gm, '### 新增项')
    .replace(/^###\s+Known limitations\s*$/gm, '### 已知限制')
    .replace(/^###\s+Removed\s*$/gm, '### 移除项')
    .replace(/^###\s+Deprecated\s*$/gm, '### 废弃项');

  return `---
title: 版本发布记录
description: 详细记录各版本更新历史与核心特性演进
---

# 版本发布记录

记录 \`image-evaluator\` 各版本核心能力演进与重要变更。

---

${body}
`;
}

async function main(): Promise<void> {
  const changelog = await fetchOrReadChangelog();
  const enContent = generateEnglishMdx(changelog);
  const zhContent = generateChineseMdx(changelog);

  fs.writeFileSync(DOCS_EN_PATH, enContent, 'utf-8');
  console.log(`Updated English changelog: ${DOCS_EN_PATH}`);

  fs.writeFileSync(DOCS_ZH_PATH, zhContent, 'utf-8');
  console.log(`Updated Chinese changelog: ${DOCS_ZH_PATH}`);

  console.log('Changelog sync completed successfully.');
}

main().catch((err: unknown) => {
  console.error('Error during changelog sync:', err);
  process.exit(1);
});
