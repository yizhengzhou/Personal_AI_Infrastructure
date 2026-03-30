# Stage 4: Export

Export final assets in all required App Store sizes and formats.

## Required Sizes (Apple App Store)

| Device | Size (px) | Required |
|--------|-----------|----------|
| iPhone 6.7" (15 Pro Max) | 1290 × 2796 | Required |
| iPhone 6.5" (14 Plus) | 1284 × 2778 | Optional (uses 6.7") |
| iPhone 5.5" (8 Plus) | 1242 × 2208 | Required if supporting |
| iPad Pro 12.9" (6th gen) | 2048 × 2732 | Required for iPad apps |
| iPad Pro 11" | 1668 × 2388 | Optional |

## Required Sizes (Google Play Store)

| Type | Size (px) | Required |
|------|-----------|----------|
| Phone | 1080 × 1920 (min) | Required |
| 7" Tablet | 1200 × 1920 | If supporting tablets |
| 10" Tablet | 1800 × 2560 | If supporting tablets |

## Process

1. **Resize**: Scale composed images to each required size
2. **Validate**: Ensure no text is cut off at smaller sizes
3. **Compress**: Optimize file size (PNG, < 8MB per image for Apple)
4. **Organize**: Structure output for upload

## Output Structure

```
{project}/assets/screenshots/export/
├── apple/
│   ├── en-US/
│   │   ├── 6.7/
│   │   │   ├── 01-hero.png
│   │   │   └── ...
│   │   └── 5.5/
│   │       └── ...
│   └── zh-Hant/
│       └── ...
└── google/
    ├── en-US/
    │   └── phone/
    │       └── ...
    └── ...
```

## Final Checklist

- [ ] All required device sizes generated
- [ ] All target locales have complete sets
- [ ] File sizes within platform limits
- [ ] No text truncation at any size
- [ ] Filenames follow platform upload conventions
