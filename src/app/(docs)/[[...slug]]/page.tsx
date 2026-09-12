import fs from 'node:fs';
import { source } from '@/lib/source';
import {
  DocsBody,
  DocsDescription,
  DocsPage,
  DocsTitle,
} from 'fumadocs-ui/page';
import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { useMDXComponents } from '@/mdx-components';

export default async function Page(props: {
  params: Promise<{ slug?: string[] }>;
}) {
  const { slug = [] } = await props.params;
  const isZh = slug[0] === 'zh';
  const lang = isZh ? 'zh' : 'en';
  const pageSlug = isZh ? slug.slice(1) : slug;
  const page = source.getPage(pageSlug, lang);
  if (!page) {
    notFound();
  }

  const MDX = page.data.body;

  let lastModified: Date | undefined;
  try {
    if (page.data._file?.absolutePath && fs.existsSync(page.data._file.absolutePath)) {
      lastModified = fs.statSync(page.data._file.absolutePath).mtime;
    }
  } catch {
    lastModified = undefined;
  }

  return (
    <DocsPage
      toc={page.data.toc}
      full={page.data.full}
      lastUpdate={lastModified}
      editOnGithub={{
        owner: 'image-evaluator',
        repo: 'docs',
        sha: 'main',
        path: `content/docs/${page.data._file.path}`,
      }}
    >
      <DocsTitle>{page.data.title}</DocsTitle>
      <DocsDescription>{page.data.description}</DocsDescription>
      <DocsBody>
        <MDX components={useMDXComponents()} />
      </DocsBody>
    </DocsPage>
  );
}

export async function generateStaticParams() {
  const enPages = source.getPages('en').map((p) => ({
    slug: p.slugs,
  }));
  const zhPages = source.getPages('zh').map((p) => ({
    slug: ['zh', ...p.slugs],
  }));
  return [...enPages, ...zhPages];
}

export async function generateMetadata(props: {
  params: Promise<{ slug?: string[] }>;
}): Promise<Metadata> {
  const { slug = [] } = await props.params;
  const isZh = slug[0] === 'zh';
  const lang = isZh ? 'zh' : 'en';
  const pageSlug = isZh ? slug.slice(1) : slug;
  const page = source.getPage(pageSlug, lang);
  if (!page) {
    notFound();
  }

  return {
    title: page.data.title,
    description: page.data.description,
  };
}

