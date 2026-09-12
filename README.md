# Image Evaluator Documentation Site

Official documentation website and interactive visual evaluation playground for [image-evaluator](https://github.com/image-evaluator/image-evaluator).

## Features

- **Next.js 15 + Fumadocs 15 + Tailwind CSS 4**: Modern, responsive, accessible documentation layout with dark mode and full-text search.
- **Authoritative 9-Metric Knowledge Base**: Detailed mathematical formulations, boundary warnings, and CLI reproduction guides for Aesthetic, CLIP, ArcFace, LPIPS, SSIM, PSNR, FID, KID, and PickScore.
- **Dogfood Interactive Playground**: Pure React pointer-captured image comparison sliders and side-by-side verification components embedding real evaluated benchmark pairs.
- **Level 0 AI-Ready Endpoints**: Automatically builds `/llms.txt` and `/llms-full.txt` (48.5KB plain markdown) tailored for 512K-context LLM ingestion.
- **Cloudflare Worker & AI Assistant**: Integrated `agnes-2.5-flash` edge streaming proxy with offline Level 0 fallback resilience.

## Local Development

```bash
bun install
bun run dev

```

Visit `http://localhost:3000` in your browser.

## Static Build & AI Export

```bash
bun run build:llms
bun run build

```

The production static HTML and machine-readable endpoints will be generated in `./out`.

## Architecture & License

Apache-2.0 License. Maintained under the [image-evaluator](https://github.com/image-evaluator) organization.
