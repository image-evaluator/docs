'use client';

import React, { useState, useRef, useCallback } from 'react';
import { SlidersHorizontal, Columns2 } from 'lucide-react';

export interface ImageComparisonProps {
  beforeImage: string;
  afterImage: string;
  beforeLabel?: string;
  afterLabel?: string;
  alt?: string;
  initialSliderPosition?: number;
  initialMode?: 'slider' | 'side-by-side';
  className?: string;
}

export function ImageComparison({
  beforeImage,
  afterImage,
  beforeLabel = '参考原图',
  afterLabel = '待测生成图',
  alt = '图像对比视图',
  initialSliderPosition = 50,
  initialMode = 'slider',
  className = '',
}: ImageComparisonProps) {
  const [mode, setMode] = useState<'slider' | 'side-by-side'>(initialMode);
  const [sliderPosition, setSliderPosition] = useState<number>(initialSliderPosition);
  const [isDragging, setIsDragging] = useState<boolean>(false);
  const containerRef = useRef<HTMLDivElement>(null);

  const updatePosition = useCallback((clientX: number) => {
    if (!containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    const rawPos = ((clientX - rect.left) / rect.width) * 100;
    const clampedPos = Math.max(0, Math.min(100, rawPos));
    setSliderPosition(clampedPos);
  }, []);

  const handlePointerDown = useCallback(
    (e: React.PointerEvent<HTMLDivElement>) => {
      setIsDragging(true);
      updatePosition(e.clientX);
      e.currentTarget.setPointerCapture(e.pointerId);
    },
    [updatePosition]
  );

  const handlePointerMove = useCallback(
    (e: React.PointerEvent<HTMLDivElement>) => {
      if (!isDragging) return;
      updatePosition(e.clientX);
    },
    [isDragging, updatePosition]
  );

  const handlePointerUp = useCallback(
    (e: React.PointerEvent<HTMLDivElement>) => {
      if (!isDragging) return;
      setIsDragging(false);
      try {
        e.currentTarget.releasePointerCapture(e.pointerId);
      } catch {
        /* Pointer capture already released */
      }
    },
    [isDragging]
  );

  const handleKeyDown = useCallback((e: React.KeyboardEvent<HTMLDivElement>) => {
    if (e.key === 'ArrowLeft') {
      e.preventDefault();
      setSliderPosition((prev) => Math.max(0, prev - 2));
    } else if (e.key === 'ArrowRight') {
      e.preventDefault();
      setSliderPosition((prev) => Math.min(100, prev + 2));
    } else if (e.key === 'Home') {
      e.preventDefault();
      setSliderPosition(0);
    } else if (e.key === 'End') {
      e.preventDefault();
      setSliderPosition(100);
    }
  }, []);

  return (
    <div className={`w-full flex flex-col gap-3 my-6 ${className}`}>
      {/* 视图模式切换控制栏 */}
      <div className="flex items-center justify-between px-1">
        <div className="flex items-center gap-2 text-xs text-neutral-500 dark:text-neutral-400 font-medium">
          <span>视图模式：</span>
          <span className="text-neutral-800 dark:text-neutral-200 font-semibold">
            {mode === 'slider' ? '双层滑块对比' : '左右并排对比'}
          </span>
        </div>
        <div className="inline-flex items-center p-0.5 rounded-lg border border-neutral-200 bg-neutral-100 dark:border-neutral-800 dark:bg-neutral-900 text-xs">
          <button
            type="button"
            onClick={() => setMode('slider')}
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded-md font-medium transition-all cursor-pointer ${
              mode === 'slider'
                ? 'bg-white text-neutral-900 shadow-xs dark:bg-neutral-800 dark:text-neutral-100'
                : 'text-neutral-600 hover:text-neutral-900 dark:text-neutral-400 dark:hover:text-neutral-200'
            }`}
          >
            <SlidersHorizontal className="h-3.5 w-3.5" />
            <span>滑块对比</span>
          </button>
          <button
            type="button"
            onClick={() => setMode('side-by-side')}
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded-md font-medium transition-all cursor-pointer ${
              mode === 'side-by-side'
                ? 'bg-white text-neutral-900 shadow-xs dark:bg-neutral-800 dark:text-neutral-100'
                : 'text-neutral-600 hover:text-neutral-900 dark:text-neutral-400 dark:hover:text-neutral-200'
            }`}
          >
            <Columns2 className="h-3.5 w-3.5" />
            <span>并排视图</span>
          </button>
        </div>
      </div>

      {mode === 'slider' ? (
        /* 交互滑块对比视图 */
        <div
          ref={containerRef}
          onPointerDown={handlePointerDown}
          onPointerMove={handlePointerMove}
          onPointerUp={handlePointerUp}
          onPointerCancel={handlePointerUp}
          className="relative aspect-square w-full max-w-2xl mx-auto overflow-hidden rounded-xl border border-neutral-200 bg-neutral-950 dark:border-neutral-800 select-none cursor-ew-resize touch-none shadow-sm"
        >
          {/* 参考原图（底层完整呈现） */}
          <img
            src={beforeImage}
            alt={`${alt} - ${beforeLabel}`}
            className="absolute inset-0 h-full w-full object-contain pointer-events-none"
          />

          {/* 待测生成图（上层基于 clipPath 动态裁剪，暴露右半区） */}
          <img
            src={afterImage}
            alt={`${alt} - ${afterLabel}`}
            className="absolute inset-0 h-full w-full object-contain pointer-events-none"
            style={{ clipPath: `inset(0 0 0 ${sliderPosition}%)` }}
          />

          {/* 参考原图徽章（左上） */}
          <div className="absolute top-3 left-3 px-2.5 py-1 rounded-md bg-black/65 backdrop-blur-md text-xs font-medium text-white shadow-xs pointer-events-none">
            {beforeLabel}
          </div>

          {/* 待测生成图徽章（右上） */}
          <div className="absolute top-3 right-3 px-2.5 py-1 rounded-md bg-black/65 backdrop-blur-md text-xs font-medium text-white shadow-xs pointer-events-none">
            {afterLabel}
          </div>

          {/* 拖动分割中线与控制手柄 */}
          <div
            tabIndex={0}
            role="slider"
            aria-label="图像对比滑块"
            aria-valuenow={Math.round(sliderPosition)}
            aria-valuemin={0}
            aria-valuemax={100}
            onKeyDown={handleKeyDown}
            className="absolute top-0 bottom-0 w-0.5 bg-white shadow-[0_0_10px_rgba(0,0,0,0.5)] cursor-ew-resize focus:outline-none"
            style={{ left: `${sliderPosition}%` }}
          >
            <div className="absolute top-1/2 -translate-x-1/2 -translate-y-1/2 flex items-center justify-center h-8 w-8 rounded-full bg-white text-neutral-800 shadow-md border border-neutral-200 dark:bg-neutral-800 dark:text-neutral-100 dark:border-neutral-700 pointer-events-none">
              <div className="flex items-center gap-0.5">
                <span className="inline-block w-0.5 h-3 bg-neutral-400 rounded-full" />
                <span className="inline-block w-0.5 h-3 bg-neutral-400 rounded-full" />
              </div>
            </div>
          </div>

          {/* 底部居中分割百分比胶囊 */}
          <div className="absolute bottom-3 left-1/2 -translate-x-1/2 px-3 py-1 rounded-full bg-black/65 backdrop-blur-md text-xs font-mono text-white shadow-xs pointer-events-none">
            {Math.round(sliderPosition)}% 分割
          </div>
        </div>
      ) : (
        /* 双图并排对照视图 */
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full max-w-4xl mx-auto">
          <div className="flex flex-col gap-2">
            <div className="flex items-center justify-between px-1">
              <span className="text-xs font-semibold text-neutral-700 dark:text-neutral-300">
                {beforeLabel}
              </span>
              <span className="text-xs font-mono text-neutral-500">基准真值</span>
            </div>
            <div className="relative aspect-square w-full overflow-hidden rounded-xl border border-neutral-200 bg-neutral-950 dark:border-neutral-800 shadow-sm">
              <img
                src={beforeImage}
                alt={`${alt} - ${beforeLabel}`}
                className="h-full w-full object-contain"
              />
            </div>
          </div>

          <div className="flex flex-col gap-2">
            <div className="flex items-center justify-between px-1">
              <span className="text-xs font-semibold text-neutral-700 dark:text-neutral-300">
                {afterLabel}
              </span>
              <span className="text-xs font-mono text-neutral-500">模型生成结果</span>
            </div>
            <div className="relative aspect-square w-full overflow-hidden rounded-xl border border-neutral-200 bg-neutral-950 dark:border-neutral-800 shadow-sm">
              <img
                src={afterImage}
                alt={`${alt} - ${afterLabel}`}
                className="h-full w-full object-contain"
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

