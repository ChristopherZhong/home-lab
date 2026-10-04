import { defineConfig } from "lint-staged/config";

export default defineConfig({
  "*.{mjs,js,jsx,mts,ts,tsx}": "prettier --write",
  "*.md": "prettier --write",
  "*.{yaml,yml}": "prettier --write",
});
