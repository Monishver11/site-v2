/* Rewrites root-relative URLs in the built Astro HTML/CSS for staging under a
   base path (e.g. /site-v2). The /notes subtree is skipped: Quartz handles its
   own base via NOTES_BASE_URL. Remove this step when the site moves to the
   domain root. Usage: BASE_PATH=/site-v2 node tooling/fix-base.mjs <dist-dir> */
import { readdirSync, readFileSync, writeFileSync, statSync } from "node:fs";
import { join } from "node:path";

const base = process.env.BASE_PATH ?? "";
const dist = process.argv[2];
if (!base || !dist) {
  console.log("BASE_PATH empty or dist missing; nothing to do");
  process.exit(0);
}

const walk = (dir) =>
  readdirSync(dir).flatMap((f) => {
    const p = join(dir, f);
    if (statSync(p).isDirectory()) {
      return f === "notes" && dir === dist ? [] : walk(p);
    }
    return /\.(html|css|xml|txt)$/.test(f) ? [p] : [];
  });

let count = 0;
for (const file of walk(dist)) {
  const src = readFileSync(file, "utf8");
  // href="/x", src="/x", url(/x) — but not protocol-relative "//host".
  const out = src
    .replace(/(href|src|content)="\/(?!\/)/g, `$1="${base}/`)
    .replace(/url\(\/(?!\/)/g, `url(${base}/`);
  if (out !== src) {
    writeFileSync(file, out);
    count++;
  }
}
console.log(`rewrote ${count} files for base ${base}`);
