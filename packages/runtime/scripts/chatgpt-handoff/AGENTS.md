# Slice issue generation

Use `../../src/runtime_promptgen/schemas/slice-manifest.schema.json` as the
authoritative contract.

For each requested slice:

1. Generate exactly one `runtime.slice.v0` manifest.
2. Validate every field against the schema.
3. Preserve the declared mutation, validation, and completion boundaries.
4. Use normalized POSIX repository-relative mutation paths. Do not use absolute
   paths, repeated separators, or `.`/`..` segments.
5. Use `null` for an absent predecessor or successor.
6. Create or update the GitHub child issue with the manifest as its complete body.
7. Pretty-print the JSON and prefix every line with four spaces so GitHub renders the pure JSON body as an indented code block.
8. Do not wrap the manifest in Markdown or a fenced code block.
9. Do not add prose outside the JSON document.
10. Preserve the complete issue body as directly parseable JSON; leading indentation is permitted JSON whitespace.
11. ChatGPT owns issue creation, updating, linking, and closure.
12. Repository tooling is read-only with respect to GitHub issues.
