import { docs } from '@/.source';
import { loader } from 'fumadocs-core/source';
import type { InferPageType } from 'fumadocs-core/source';
import { i18n } from '@/lib/i18n';

const rawSource = docs.toFumadocsSource();
const files = typeof rawSource.files === 'function'
  ? (rawSource.files as unknown as () => any)()
  : rawSource.files;

export const source = loader({
  baseUrl: '/',
  i18n,
  source: {
    ...rawSource,
    files,
  } as typeof rawSource,
});

export type Page = InferPageType<typeof source>;


