# Screenshot Pipeline

Automated pipeline for creating App Store marketing screenshots from real app captures.

## Overview

This pipeline uses Mirroir MCP to capture real device screenshots, then composes them into marketing-grade App Store assets using the Media skill.

## Prerequisites

- Mirroir MCP connected to iOS Simulator or physical device
- Media skill available for image composition
- Project has an `app-marketing-context.md` with brand colors, slogan, target audience

## Pipeline Stages

| Stage | File | Tool | Input | Output |
|-------|------|------|-------|--------|
| 1. Capture | `1-Capture.md` | Mirroir MCP | Running app on device | Raw PNG screenshots |
| 2. Compose | `2-Compose.md` | Media skill | Raw screenshots + brand context | Marketing-grade images |
| 3. Localize | `3-Localize.md` | Media skill | Composed images + translations | Localized variants |
| 4. Export | `4-Export.md` | Image tools | Localized images | App Store-ready assets per device |

## Quick Start

1. Ensure your app is running on simulator/device
2. Have `app-marketing-context.md` in your project root
3. Invoke: `/app-store-optimization` → select ScreenshotPipeline
4. Pipeline will guide you through each stage
