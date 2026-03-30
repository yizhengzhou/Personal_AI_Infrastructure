# Stage 3: Localize

Create localized variants of composed screenshots for target markets.

## Prerequisites

- Composed screenshots from Stage 2
- Target locales defined in `app-marketing-context.md`
- Translated headline text per locale

## Process

1. **Identify target locales**: Read from marketing context (default: en, zh-Hant, ja)
2. **Translate headlines**: For each screenshot, translate the headline text
3. **Re-compose**: Use Media skill to replace text layer with localized version
4. **Validate**: Check text fits within layout, adjust font size if needed

## Localization Checklist

- [ ] All headline text translated and reviewed
- [ ] Font supports target language characters (CJK, Arabic, etc.)
- [ ] Text direction correct (RTL for Arabic/Hebrew)
- [ ] Cultural appropriateness of imagery verified
- [ ] Date/number formats localized if visible in screenshots

## Common Locale Priorities

| Priority | Locales | Reason |
|----------|---------|--------|
| Tier 1 | en-US, zh-Hant, ja | Highest revenue markets |
| Tier 2 | ko, de, fr, es | Strong app markets |
| Tier 3 | pt-BR, it, ru, ar | Growing markets |

## Output

Save to: `{project}/assets/screenshots/localized/{locale}/`
Naming: `{locale}-{nn}-{screen-name}.png`
