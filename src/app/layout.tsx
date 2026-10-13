import type { Metadata } from 'next';
import { RootProvider } from 'fumadocs-ui/provider';
import { CustomSearchDialog } from '@/components/SearchDialog';
import 'katex/dist/katex.css';
import './global.css';

export const metadata: Metadata = {
  title: {
    template: '%s | image-evaluator',
    default: 'image-evaluator | Image Quality and Alignment Evaluation',
  },
  description: 'Enterprise-grade evaluation suite for AI image generation covering 15 metrics with Python SDK and CLI interfaces.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="font-sans" suppressHydrationWarning>
      <body className="flex flex-col min-h-screen">
        <RootProvider search={{ SearchDialog: CustomSearchDialog }}>
          {children}
        </RootProvider>
      </body>
    </html>
  );
}

