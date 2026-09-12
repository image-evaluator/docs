import defaultMdxComponents from 'fumadocs-ui/mdx';
import { Accordion, Accordions } from 'fumadocs-ui/components/accordion';
import { Step, Steps } from 'fumadocs-ui/components/steps';
import { ImageComparison } from '@/components/ImageComparison';
import { MetricVisualShowcase } from '@/components/MetricVisualShowcase';
import type { MDXComponents } from 'mdx/types';

export function useMDXComponents(components?: MDXComponents): MDXComponents {
  return {
    ...defaultMdxComponents,
    Accordion,
    Accordions,
    Step,
    Steps,
    ImageComparison,
    MetricVisualShowcase,
    ...components,
  };
}


