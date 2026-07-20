import { defineConfig } from "astro/config";
import remarkMath from "remark-math";
import remarkDirective from "remark-directive";
import rehypeKatex from "rehype-katex";
import remarkSidenote from "./src/plugins/remark-sidenote.mjs";

export default defineConfig({
  site: "https://monishver11.github.io",
  output: "static",
  markdown: {
    remarkPlugins: [remarkMath, remarkDirective, remarkSidenote],
    rehypePlugins: [rehypeKatex],
    shikiConfig: {
      theme: "vitesse-light",
    },
  },
});
