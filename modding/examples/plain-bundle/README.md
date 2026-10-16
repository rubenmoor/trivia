# Example: plain bundle

A question bundle in the plain format: each subcategory name in `categories.json` is its own key, the category's `name` its name, no names files. Three Spanish questions about dinosaurs. The bundle template (`../../template-bundle/`) shows the other format, slugs + `names.<locale>.json`; both are described in `../../bundles.md`.

## Try it
- Copy `plain-bundle/` into the mods folder (`../../README.md`), restart, choose «Dinosaurios» before a game.
- Check: `living-room-trivia --check-mod plain-bundle`
