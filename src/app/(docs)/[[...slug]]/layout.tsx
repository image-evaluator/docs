import { source } from '@/lib/source';
import { DocsLayout } from 'fumadocs-ui/layouts/docs';
import { I18nLayoutProvider } from '@/components/I18nLayoutProvider';
import type { ReactNode } from 'react';

export default async function RootDocsLayout(props: {
  params: Promise<{ slug?: string[] }>;
  children: ReactNode;
}) {
  const { slug = [] } = await props.params;
  const isZh = slug[0] === 'zh';
  const lang = isZh ? 'zh' : 'en';
  const tree = source.pageTree[lang];

  return (
    <I18nLayoutProvider locale={lang}>
      <DocsLayout
        tree={tree}
        githubUrl="https://github.com/neverbiasu/image-evaluator"
        i18n={true}
        nav={{
          title: 'image-evaluator',
          url: isZh ? '/zh' : '/',
        }}
        links={[
          {
            text: isZh ? '实测演练' : 'Visual Benchmark',
            url: isZh ? '/zh/benchmark/visual-demo' : '/benchmark/visual-demo',
          },
        ]}
      >
        {props.children}
      </DocsLayout>
    </I18nLayoutProvider>
  );
}


