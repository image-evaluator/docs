'use client';

import React from 'react';

export interface ScaleSegment {
  label: string;
  range: [number, number];
  color: 'emerald' | 'amber' | 'rose' | 'blue';
  note?: string;
}

export interface MetricScaleProps {
  min: number;
  max: number;
  unit?: string;
  direction: 'higher' | 'lower';
  segments: ScaleSegment[];
  currentValue?: number;
  currentLabel?: string;
}

const colorMap = {
  emerald: 'bg-emerald-500/20 text-emerald-700 dark:text-emerald-300 border-emerald-500/40',
  amber: 'bg-amber-500/20 text-amber-700 dark:text-amber-300 border-amber-500/40',
  rose: 'bg-rose-500/20 text-rose-700 dark:text-rose-300 border-rose-500/40',
  blue: 'bg-blue-500/20 text-blue-700 dark:text-blue-300 border-blue-500/40',
};

const barColorMap = {
  emerald: 'bg-emerald-500',
  amber: 'bg-amber-500',
  rose: 'bg-rose-500',
  blue: 'bg-blue-500',
};

export function MetricScale({
  min,
  max,
  unit = '',
  direction,
  segments,
  currentValue,
  currentLabel,
}: MetricScaleProps) {
  const span = max - min;
  const isLowerBetter = direction === 'lower';

  return (
    <div className="my-6 p-4 rounded-xl border border-fd-border bg-fd-card/50 text-fd-card-foreground shadow-xs">
      <div className="flex items-center justify-between text-xs font-medium text-fd-muted-foreground mb-2">
        <span className="font-mono">
          Scale: {min}{unit} → {max}{unit}
        </span>
        <span
          className={`px-2 py-0.5 rounded-full border text-[11px] font-semibold ${
            isLowerBetter
              ? 'bg-blue-500/10 text-blue-600 dark:text-blue-400 border-blue-500/30'
              : 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/30'
          }`}
        >
          {isLowerBetter ? 'Lower is Better ↓' : 'Higher is Better ↑'}
        </span>
      </div>

      {/* Progress Track */}
      <div className="relative h-3 rounded-full bg-fd-secondary overflow-hidden flex w-full">
        {segments.map((seg, idx) => {
          const segWidth = ((seg.range[1] - seg.range[0]) / span) * 100;
          return (
            <div
              key={idx}
              style={{ width: `${Math.max(0, Math.min(100, segWidth))}%` }}
              className={`h-full ${barColorMap[seg.color]} transition-all opacity-85`}
              title={`${seg.label}: ${seg.range[0]} - ${seg.range[1]}${unit}`}
            />
          );
        })}
      </div>

      {/* Segments Legend */}
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 mt-3 text-xs">
        {segments.map((seg, idx) => (
          <div
            key={idx}
            className={`p-2 rounded-lg border text-center ${colorMap[seg.color]}`}
          >
            <div className="font-semibold text-[11px]">{seg.label}</div>
            <div className="font-mono text-[10px] opacity-80 mt-0.5">
              {seg.range[0]} - {seg.range[1]} {unit}
            </div>
            {seg.note && (
              <div className="text-[10px] mt-1 opacity-70 leading-tight">
                {seg.note}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

