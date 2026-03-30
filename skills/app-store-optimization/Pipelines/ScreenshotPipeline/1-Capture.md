# Stage 1: Capture

Capture real app screenshots from device using Mirroir MCP.

## Process

1. **List targets**: Use `mcp__mirroir__list_targets` to find connected devices/simulators
2. **Switch to target**: Use `mcp__mirroir__switch_target` to select the device
3. **Navigate to screen**: Use `mcp__mirroir__tap`, `mcp__mirroir__swipe`, `mcp__mirroir__type_text` to navigate to each key screen
4. **Capture screenshot**: Use `mcp__mirroir__screenshot` for each screen

## Recommended Captures

Based on App Store best practices (first 3 screenshots are most critical):

1. **Hero screen** — The primary value proposition / main feature
2. **Key feature 1** — Most compelling secondary feature
3. **Key feature 2** — Third most important feature
4. **Social proof / results** — Show outcomes or community
5. **Onboarding / getting started** — Low barrier to entry message
6. **Additional features** — Up to 10 total for App Store

## Tips

- Capture at highest resolution available (prefer iPhone 15 Pro Max / 6.7")
- Use realistic demo data, not empty states
- Capture both light and dark mode if supported
- Ensure status bar shows ideal state (full battery, good signal, clean time)

## Output

Save captures to: `{project}/assets/screenshots/raw/`
Naming: `{nn}-{screen-name}.png` (e.g., `01-hero.png`, `02-feature-search.png`)
