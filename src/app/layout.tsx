import type { Metadata } from 'next';
import { RootProvider } from 'fumadocs-ui/provider';
import { CustomSearchDialog } from '@/components/SearchDialog';
import 'katex/dist/katex.css';
import './global.css';

export const metadata: Metadata = {
  title: {
    template: '%s | image-evaluator',
    default: 'image-evaluator | Unified Image Quality & Multidimensional Alignment Toolkit',
  },
  description: 'Production-grade multidimensional evaluation toolkit for AI image generation covering 9 core metrics with Python API & CLI.',
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

