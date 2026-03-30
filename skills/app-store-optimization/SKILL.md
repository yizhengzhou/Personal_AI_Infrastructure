---
name: app-store-optimization
description: Complete App Store Optimization (ASO) toolkit for researching, optimizing, and tracking mobile app performance on Apple App Store and Google Play Store. Includes automated screenshot pipeline via Mirroir MCP. ASO優化, 商店排名, 應用商店優化.
---

# App Store Optimization (ASO)

Comprehensive ASO toolkit with 15 specialized workflows and an automated screenshot pipeline.

## Customization

**Before executing, check for user customizations at:**
`~/.claude/PAI/USER/SKILLCUSTOMIZATIONS/AppStoreOptimization/`

If this directory exists, load and apply any PREFERENCES.md, configurations, or resources found there.

## First Step: Marketing Context

Before any ASO work, check if the project has an `app-marketing-context.md` in its root. If not, run the **AppMarketingContext** workflow first — all other workflows depend on it.

## Workflow Routing

Route to the appropriate workflow based on the user's request.

| Trigger | Workflow |
|---------|----------|
| keyword research, find keywords, search volume, keyword difficulty | `Workflows/KeywordResearch.md` |
| optimize title, ASO metadata, keyword field, app description, subtitle | `Workflows/MetadataOptimization.md` |
| screenshots, app preview, product page design, screenshot pipeline | `Workflows/ScreenshotOptimization.md` |
| competitor analysis, competitive research, keyword gap | `Workflows/CompetitorAnalysis.md` |
| app launch, launch plan, launch checklist, pre-launch | `Workflows/AppLaunch.md` |
| retention, churn, engagement, DAU/MAU, user activation | `Workflows/RetentionOptimization.md` |
| reviews, ratings, negative reviews, rating dropping | `Workflows/ReviewManagement.md` |
| analytics, tracking, metrics, KPIs, funnel, attribution | `Workflows/AppAnalytics.md` |
| ASO audit, ASO score, why not ranking, listing review | `Workflows/AsoAudit.md` |
| A/B test, product page optimization, test screenshots, CPP | `Workflows/AbTestStoreListing.md` |
| localization, translate, international markets, expand countries | `Workflows/Localization.md` |
| pricing, paywall, subscription, IAP, monetize, revenue | `Workflows/MonetizationStrategy.md` |
| app context, marketing brief, app positioning | `Workflows/AppMarketingContext.md` |
| get featured, App Store editorial, App of the Day | `Workflows/AppStoreFeatured.md` |
| Apple Search Ads, user acquisition, paid ads, UA, ad campaign | `Workflows/UaCampaign.md` |

## Pipelines

Automated multi-step pipelines that combine MCP tools and skills.

| Trigger | Pipeline |
|---------|----------|
| screenshot pipeline, automated screenshots, create App Store screenshots, marketing screenshots from device | `Pipelines/ScreenshotPipeline/README.md` |

### Screenshot Pipeline Overview

Captures real device screenshots via **Mirroir MCP**, composes marketing-grade images via **Media skill**, localizes text, and exports in all required App Store sizes.

Stages: **Capture** → **Compose** → **Localize** → **Export**

See `Pipelines/ScreenshotPipeline/README.md` for full details.

## References

| Reference | Content |
|-----------|---------|
| `References/AppStoreSpecs.md` | Device screenshot sizes, metadata character limits, icon specs |

## Cross-Workflow Navigation

Many workflows reference each other. Common paths:

```
AppMarketingContext (foundation)
    ├── KeywordResearch → MetadataOptimization
    ├── CompetitorAnalysis → KeywordResearch
    ├── ScreenshotOptimization → AbTestStoreListing
    ├── AsoAudit → (routes to specific workflows based on findings)
    └── AppLaunch → (orchestrates multiple workflows)
```

## Integration with Other Skills

- **Media**: For composing marketing screenshots and visual assets
- **agent-device / Mirroir MCP**: For capturing real device screenshots
- **Research**: For market research and trend analysis
- **Localization workflow**: For multi-language metadata and screenshots
