import Link from 'next/link';

export default function HomePage() {
  return (
    <main className="flex flex-1 flex-col items-center justify-center p-6 text-center">
      <h1 className="text-4xl font-extrabold tracking-tight sm:text-5xl">
        image-evaluator
      </h1>
      <p className="mt-4 max-w-2xl text-lg text-fd-muted-foreground">
        轻量统一的图像质量与对齐评估套件，涵盖 9 项主流指标，支持 Python API 与 CLI 极速评测。
      </p>
      <div className="mt-8 flex gap-4">
        <Link
          href="/docs"
          className="rounded-lg bg-fd-primary px-5 py-2.5 font-medium text-fd-primary-foreground transition-opacity hover:opacity-90"
        >
          查看文档
        </Link>
      </div>
    </main>
  );
}

