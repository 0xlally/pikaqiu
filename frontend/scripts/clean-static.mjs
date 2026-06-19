import { rm } from "node:fs/promises";
import { resolve } from "node:path";

const staticRoot = resolve(import.meta.dirname, "../../pikaqiu_agent/static");
const targets = [
  resolve(staticRoot, "assets"),
  resolve(staticRoot, "app.js"),
  resolve(staticRoot, "styles.css")
];

await Promise.all(targets.map((target) => rm(target, { recursive: true, force: true })));
