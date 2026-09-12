import type { Metadata } from 'next';
import { RootProvider } from 'fumadocs-ui/provider';
import 'katex/dist/katex.css';
import './global.css';

export const metadata: Metadata = {
  title: {
    template: '%s | image-evaluator',
    default: 'image-evaluator | 统一图像质量与对齐评估套件',
  },
  description: '轻量统一的图像质量与多维对齐评估套件，涵盖 9 项主流指标，支持 Python API 与 CLI 极速评测。',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh" className="font-sans" suppressHydrationWarning>
      <body className="flex flex-col min-h-screen">
        <RootProvider>{children}</RootProvider>
      </body>
    </html>
  );
}

