import fs from "node:fs";
import path from "node:path";
const root = process.cwd();
const expected = path.normalize("contracts/PrecedentKernel.py");
const ignored = new Set([".git", "node_modules", ".pytest_cache", "__pycache__", "artifacts"]);
const files: string[] = [];
function walk(dir: string): void {
  for (const entry of fs.readdirSync(dir, {withFileTypes: true})) {
    if (ignored.has(entry.name)) continue;
    const absolute = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(absolute);
    else if (entry.isFile() && entry.name.endsWith(".py")) files.push(path.normalize(path.relative(root, absolute)));
  }
}
walk(root);
const candidates = files.filter((file) => {
  const source = fs.readFileSync(path.join(root, file), "utf8");
  return /["']Depends["']\s*:|\bgl\.Contract\b|\bfrom\s+genlayer\s+import\b/.test(source);
});
if (candidates.length !== 1 || candidates[0] !== expected) throw new Error(`Expected only ${expected}; got ${candidates}`);
console.log(`Contract discovery passed: ${expected}`);
