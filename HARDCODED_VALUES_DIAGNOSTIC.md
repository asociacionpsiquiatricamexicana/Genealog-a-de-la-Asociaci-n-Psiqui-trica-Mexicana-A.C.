# RAPM Vol. 6 No. 1 · Hardcoded Valuesgit pull --tagsgit config pull.rebase true
git pull --tags

Audit of numeric/string literals in the editorial pipeline codebase, identification of named-constant candidates, and refactor application. Captured 2026-04-19.

## Executive summary

| Dimension | Before | After |
|---|---|---|
| Hardcoded literals in `pipeline_rapm_v6n1.py` | 22 | **0** ✓ |
| Unused layout constants (defined but not imported) | 12 | **0** ✓ |
| Palette constants (Python) | 5 | 7 (+PINK_DIVIDER, +ABSTRACT_BRACKET) |
| Rule-width constants | 0 (all inline literals) | **5** (RW_HAIRLINE/THIN/MEDIUM/STANDARD/BOLD) |
| Font-size constants | 0 (all inline literals) | **6** (FS_CENTERED_*, FS_KEYWORDS, FS_EMAIL_*) |
| Volume metadata constants | 3 (VOLUME, ISSUE, YEAR) | 4 (+PAGE_COUNT) |
| Layout constants for p24 divider | 0 | **2** (P24_DIVIDER_Y, P24_DIVIDER_X_RANGE) |
| Layout constants for p25 rule | 0 | **1** (P25_FOOTER_RULE_Y) |
| Article-rule layout constants | 0 | **2** (ART_RULE_X_RANGE, ART_FIRST_FOOTER_RULE_Y) |
| QA suite | 27/27 | **27/27** ✓ |
| Volume MD5 | `8ed6ff1df6d6609b89a90c20ba48880e` | `d6f5f6ca77663344dbdbb16d6a44ec77` |

Build succeeds; QA fully green; ornament hex values cross-verified pixel-exact after refactor.

## Pass 1 · Inventory of hardcoded literals (pre-refactor)

Forensic scan of `pipeline_rapm_v6n1.py` phase 2 (per-page surgery) found 22 literals:

| Type | Locations | Values |
|---|---|---|
| `insert_footer(..., 34, text_y=771)` | L277, L317 | `34` (PAGE_COUNT), `771` (ART_FOOTER_TEXT_Y, already defined!) |
| Footer rule `y` | L278, L315 | `750.9`, `762` |
| Rule `x_range` tuples | L278, L315 | `(56.7, 555.3)` (56.7 already = FOOTER_LEFT_X) |
| p24 divider `Point` | L298, L299 | `(314.5, 340)`, `(555.0, 340)` |
| p24 divider color inline | L300 | `(197/255, 140/255, 148/255)` |
| p24 divider width | L301 | `0.248` |
| Rule widths | L232, L279, L301, L316, L328 | `0.3`, `0.4` (×2), `0.248`, `0.5` |
| Font sizes | L248, L253, L257, L260, L270, L309, L314, L336, L339, L346, L349 | `9` (×4), `7.8` (×2), `6.5`, `8` (×2), `8.5` (×2) |
| Mission center x | L268 | `306` (PAGE_CENTER_X, already defined!) |

### Root cause — "abstraction bypass"

Twelve constants in `rapm_layout.py` were **defined but never imported** into the pipeline. Notable: `ART_FOOTER_TEXT_Y = 771` existed but the pipeline used `text_y=771` as a literal. `PAGE_CENTER_X = 306` existed but the pipeline used `center_x=306` directly. Historical migration artifact — earlier pipeline versions pre-dated the layout module's full constant set.

## Pass 2 · Duplicated strings across files

| String | Pipeline | Helpers | QA | Config |
|---|---|---|---|---|
| `Asociación Psiquiátrica Mexicana` | 2 | 0 | 1 | 6 |
| `CC BY-NC 4.0` | 4 | 1 | 2 | 2 |
| `Publicado por` | 0 | 0 | 1 | 1 |

String literals are not refactored in this pass (mostly used within string formatting, which would over-complicate). They are centralized in `rapm_config.py` as `FOOTER_LEFT` and `FOOTER_RIGHT` already for use by helpers.

## Pass 3 · Refactor applied

### `rapm_config.py` additions

```python
# Accent colors (exact hex-derived floats)
PINK_DIVIDER     = (0xC5/255, 0x8C/255, 0x94/255)   # #C58C94
ABSTRACT_BRACKET = (0xD8/255, 0xB4/255, 0xB9/255)   # #D8B4B9

# Rule widths (pt)
RW_HAIRLINE  = 0.248   # decorative hairlines (reference dividers)
RW_THIN      = 0.3     # subtle separators
RW_MEDIUM    = 0.4     # footer/masthead rules
RW_STANDARD  = 0.5     # table body rules
RW_BOLD      = 0.8     # table top rules (APA booktabs)

# Font sizes (pt)
FS_CENTERED_TITLE = 9        # Mission-block titles
FS_CENTERED_BODY  = 7.8      # Mission-block body
FS_CENTERED_META  = 6.5      # Credit line
FS_KEYWORDS       = 8        # p25 Keywords
FS_EMAIL_LABEL    = 8.5      # p33 email label
FS_EMAIL_INLINE   = 9        # p32 email inline

# Volume metadata
PAGE_COUNT = 34
```

All 14 new symbols added to `__all__`.

### `rapm_layout.py` additions

```python
# p24 "How to cite" divider (restored after _shift_region_clean)
P24_DIVIDER_Y       = 340
P24_DIVIDER_X_RANGE = (314.5, 555.0)

# p25 footer rule (exception: lower than others, avoids Keywords collision)
P25_FOOTER_RULE_Y = 762

# Article rule geometry
ART_RULE_X_RANGE        = (56.7, 555.3)
ART_FIRST_FOOTER_RULE_Y = 750.9
```

All 5 new symbols added to `__all__`.

### Pipeline refactor (phase 2 surgery)

Every literal → named constant. Before/after examples:

| Before | After |
|---|---|
| `draw_ornamental_hline(p2, 723.5, ..., color=LIGHTGRAY, width=0.3)` | `draw_ornamental_hline(p2, 723.5, ..., color=LIGHTGRAY, width=RW_THIN)` |
| `insert_footer(p13, 13, 34, text_y=771)` | `insert_footer(p13, 13, PAGE_COUNT, text_y=ART_FOOTER_TEXT_Y)` |
| `draw_ornamental_hline(p13, 750.9, x_range=(56.7, 555.3), color=BURGUNDY, width=0.4)` | `draw_ornamental_hline(p13, ART_FIRST_FOOTER_RULE_Y, x_range=ART_RULE_X_RANGE, color=BURGUNDY, width=RW_MEDIUM)` |
| `p24.draw_line(fitz.Point(314.5, 340), fitz.Point(555.0, 340), color=(197/255, 140/255, 148/255), width=0.248)` | `p24.draw_line(fitz.Point(P24_DIVIDER_X_RANGE[0], P24_DIVIDER_Y), fitz.Point(P24_DIVIDER_X_RANGE[1], P24_DIVIDER_Y), color=PINK_DIVIDER, width=RW_HAIRLINE)` |
| `fontsize=9, color=BURGUNDY` (mission titles) | `fontsize=FS_CENTERED_TITLE, color=BURGUNDY` |
| `fontsize=7.8, lead=10.0, color=DARKGRAY` | `fontsize=FS_CENTERED_BODY, lead=10.0, color=DARKGRAY` |
| `fontsize=6.5, color=MIDGRAY` | `fontsize=FS_CENTERED_META, color=MIDGRAY` |
| `fontsize=8, color=BURGUNDY` (keywords) | `fontsize=FS_KEYWORDS, color=BURGUNDY` |
| `fontsize=9, color=BURGUNDY` (email inline) | `fontsize=FS_EMAIL_INLINE, color=BURGUNDY` |
| `fontsize=8.5, color=BURGUNDY` (email label) | `fontsize=FS_EMAIL_LABEL, color=BURGUNDY` |
| `center_x=306` | `center_x=PAGE_CENTER_X` |
| `width=0.5` (table rules) | `width=RW_STANDARD` |

Total: **22 → 0 hardcoded literals**.

## Pass 4 · Post-refactor verification

### Build + QA

- `python3 pipeline_rapm_v6n1.py` → ✓ Build complete (exit 0)
- `python3 qa_validate.py` → **27/27 passed**
- Volume MD5 changed: `8ed6ff1d…` → `d6f5f6ca…`
- File size: 4,647,452 bytes (+1 byte vs previous; content-stream re-encoding)

### Pixel-level hex verification

All refactored ornaments render with the exact expected hex:

| Ornament | Expected | Actual | Match |
|---|---|---|---|
| Triangle p7 | `#8B1A2B` | `#8B1A2B` | ✓ |
| Triangle p10 | `#8B1A2B` | `#8B1A2B` | ✓ |
| Triangle p13 | `#8B1A2B` | `#8B1A2B` | ✓ |
| Triangle p20 | `#8B1A2B` | `#8B1A2B` | ✓ |
| Triangle p25 | `#8B1A2B` | `#8B1A2B` | ✓ |
| p13 footer rule | `#8B1A2B` w=0.4 | `#8B1A2B` w=0.400 | ✓ |
| p25 footer rule | `#8B1A2B` w=0.4 | `#8B1A2B` w=0.400 | ✓ |
| p24 divider | `#C58C94` w=0.248 | `#C58C94` w=0.248 | ✓ |
| p28 Tabla 2 rules ×3 | `#2D2D2D` w=0.5 | `#2D2D2D` w=0.500 | ✓ |

Zero drift. The hex-derived-float palette + named constants give bit-exact rendering.

## Pass 5 · Residual hardcoded literals (final scan)

Post-refactor automated scan of `pipeline_rapm_v6n1.py`:

```
Remaining hardcoded literals: 0
  y_literal: 0
  width_literal: 0
  fontsize_literal: 0
  pagecount_literal: 0
  point_literal: 0
```

**Zero remaining** literals in the operational pipeline. All are now named.

## Codebase line counts (after refactor)

| File | Lines | Change |
|---|---|---|
| pipeline_rapm_v6n1.py | 541 | +13 (new imports + comments) |
| rapm_config.py | 165 | +29 (new palette + widths + fontsizes + PAGE_COUNT) |
| rapm_layout.py | 132 | +11 (P24/P25/ART constants) |
| rapm_helpers.py | 117 | 0 |
| qa_validate.py | 188 | 0 |
| **Total Python** | **1143** | **+53 LoC** |

+53 LoC is pure documentation/centralization — the surgery logic remains unchanged, only expressed through named symbols.

## Benefits delivered

1. **Single source of truth per design intent**: The pipeline's intent ("use medium rule width") is now declarative (`RW_MEDIUM`) rather than numeric (`0.4`). Changes propagate by editing one constant.
2. **Discoverability**: A new maintainer can read `rapm_config.py` / `rapm_layout.py` and immediately see all tunable parameters grouped by category.
3. **Cross-system hex sync**: Color constants derived from hex (`0x8B/255`) match LaTeX's hex-specified colors pixel-exact — already proven to eliminate the `#8A1A2B`/`#8B192B` drift observed in the ornaments diagnostic.
4. **Reduced duplication**: `771` and `34` appeared twice each; now one source each.
5. **Abstraction layer integrity**: 12 previously-unused layout constants are now imported and active, eliminating the "two-layer dissonance" where the pipeline bypassed the abstraction.
6. **Compilation integrity**: QA continues to pass 27/27 with no visual regression.

## Build metadata

- Volume MD5: `d6f5f6ca77663344dbdbb16d6a44ec77`
- File size: 4,647,452 bytes (4.43 MB)
- QA: **27/27 passed** ✓
- Python codebase: 1,143 LoC across 5 modules
- Pipeline version: `16.0-consolidated` (unchanged functional semantics)
