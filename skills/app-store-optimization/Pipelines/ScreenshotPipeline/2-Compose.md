# Stage 2: Compose

Transform raw screenshots into marketing-grade App Store images.

## Prerequisites

- Raw screenshots from Stage 1 in `{project}/assets/screenshots/raw/`
- `app-marketing-context.md` with: brand colors, fonts, slogan, taglines per feature

## Process

1. **Read marketing context**: Load `app-marketing-context.md` for brand guidelines
2. **Design layout**: Use the Media skill to create marketing compositions:
   - Device frame (iPhone mockup) around the screenshot
   - Headline text above/below the device (feature benefit, not feature name)
   - Brand-consistent background (gradient, solid, or pattern)
   - Optional: badges, ratings, awards

## Layout Patterns (High-Converting)

| Pattern | Description | Best For |
|---------|-------------|----------|
| **Device Center** | Centered phone with headline above | Hero screenshot |
| **Device Angled** | Tilted phone with dynamic background | Feature highlights |
| **Split Screen** | Two phones side by side | Before/after, comparison |
| **Full Bleed** | Screenshot fills entire frame with text overlay | Immersive apps |
| **Minimal** | Small device, large text | Text-heavy value props |

## Text Guidelines

- **Headline**: 3-6 words, benefit-focused (not "Search Feature" → "Find Anything Instantly")
- **Font**: Match app's brand font, minimum 60pt for readability
- **Contrast**: Text must be readable on the background
- **Language**: Match store locale (handled in Stage 3)

## Output

Save to: `{project}/assets/screenshots/composed/`
Naming: `{nn}-{screen-name}-composed.png`
Size: 1290×2796 px (iPhone 6.7" @ 3x)
