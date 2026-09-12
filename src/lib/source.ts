import { docs } from '@/.source';
import { loader } from 'fumadocs-core/source';
import type { InferPageType } from 'fumadocs-core/source';

const rawSource = docs.toFumadocsSource();
const files = typeof rawSource.files === 'function'
  ? (rawSource.files as unknown as () => any)()
  : rawSource.files;

export const source = loader({
  baseUrl: '/',
  source: {
    ...rawSource,
    files,
  } as typeof rawSource,
});

export type Page = InferPageType<typeof source>;

