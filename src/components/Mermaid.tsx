'use client';

import React, { useEffect, useRef, useState, useId } from 'react';

interface MermaidProps {
  chart: string;
  className?: string;
}

export function Mermaid({ chart, className = '' }: MermaidProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [svgHtml, setSvgHtml] = useState<string>('');
  const [hasError, setHasError] = useState<boolean>(false);
  const rawId = useId().replace(/[^a-zA-Z0-9_-]/g, '');
  const elementId = `mermaid-${rawId}`;

  useEffect(() => {
    let isMounted = true;

    async function renderMermaid() {
      try {
        const mermaid = (await import('mermaid')).default;
        const isDark = document.documentElement.classList.contains('dark');

        mermaid.initialize({
          startOnLoad: false,
          theme: isDark ? 'dark' : 'neutral',
          securityLevel: 'loose',
          fontFamily: 'inherit',
          flowchart: {
            htmlLabels: true,
            curve: 'basis',
          },
        });

        // Clean any residual elements with same id
        const existing = document.getElementById(elementId);
        if (existing) {
          existing.remove();
        }

        const { svg } = await mermaid.render(elementId, chart.trim());
        if (isMounted) {
          setSvgHtml(svg);
          setHasError(false);
        }
      } catch (err) {
        console.error('Failed to render Mermaid chart:', err);
        if (isMounted) {
          setHasError(true);
        }
      }
    }

    renderMermaid();

    return () => {
      isMounted = false;
    };
  }, [chart, elementId]);

  if (hasError) {
    return (
      <pre className="my-6 overflow-x-auto rounded-xl border border-red-200 bg-red-50/50 p-4 font-mono text-xs text-red-700 dark:border-red-900/50 dark:bg-red-950/30 dark:text-red-400">
        <code>{chart}</code>
      </pre>
    );
  }

  if (!svgHtml) {
    return (
      <div className="my-6 flex items-center justify-center rounded-xl border border-neutral-200 bg-neutral-50/60 p-8 text-xs text-neutral-400 dark:border-neutral-800 dark:bg-neutral-900/50">
        <span>Loading diagram...</span>
      </div>
    );
  }

  return (
    <div
      ref={containerRef}
      className={`my-6 flex justify-center overflow-x-auto rounded-xl border border-neutral-200/80 bg-neutral-50/60 p-4 backdrop-blur-xs dark:border-neutral-800 dark:bg-neutral-900/40 [&_svg]:max-w-full [&_svg]:h-auto ${className}`}
      dangerouslySetInnerHTML={{ __html: svgHtml }}
    />
  );
}
