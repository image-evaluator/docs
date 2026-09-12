import { source } from '@/lib/source';
import { DocsLayout } from 'fumadocs-ui/layouts/docs';
import type { ReactNode } from 'react';
import { AIAssistant } from '@/components/AIAssistant';

export default function RootDocsLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <DocsLayout
      tree={source.pageTree}
      nav={{
        title: 'image-evaluator',
      }}
    >
      {children}
      <AIAssistant />
    </DocsLayout>
  );
}

