import { HomeLayout } from 'fumadocs-ui/layouts/home';
import type { ReactNode } from 'react';

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <HomeLayout
      nav={{
        title: 'image-evaluator',
      }}
      links={[
        {
          text: '文档中心',
          url: '/docs',
        },
        {
          text: '视觉演练 Demo',
          url: '/docs/visual-demo',
        },
        {
          text: 'GitHub',
          url: 'https://github.com/image-evaluator/image-evaluator',
          external: true,
        },
      ]}
    >
      {children}
    </HomeLayout>
  );
}
