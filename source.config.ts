import { defineConfig, defineDocs } from 'fumadocs-mdx/config';
import rehypeKatex from 'rehype-katex';
import remarkMath from 'remark-math';

function remarkMathCode() {
  return (tree: any) => {
    function walk(node: any) {
      if (!node) return;
      if (node.type === 'code' && node.lang === 'math') {
        node.type = 'math';
        node.data = {
          hName: 'pre',
          hChildren: [
            {
              type: 'element',
              tagName: 'code',
              properties: {
                className: ['language-math', 'math-display'],
              },
              children: [{ type: 'text', value: node.value.trim() }],
            },
          ],
        };
      }
      if (node.children) {
        node.children.forEach(walk);
      }
    }
    walk(tree);
  };
}

export const docs = defineDocs({
  dir: 'content/docs',
});

export default defineConfig({
  mdxOptions: {
    remarkPlugins: [remarkMath, remarkMathCode],
    rehypePlugins: (v) => [rehypeKatex, ...v],
  },
});

