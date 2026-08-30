# RAPM Vol. 6 No. 1 · Ornaments Diagnostic

Forensic inventory of all non-text graphic elements across all 34 pages: rules, frames, abstract boxes, corner triangles, table lines, figure drawings, decorative separators. Captured 2026-04-19.

## Executive summary

| Dimension | Status | Notes |
|---|---|---|
| Ornament inventory | ✓ | 34 pages catalogued, 9 distinct ornament types |
| Burgundy consistency | ✓ (post-fix) | All now exact `#8B1A2B` (was `#8A1A2B` Python + `#8B192B` LaTeX) |
| Pink accent consistency | ✓ (post-fix) | Reference divider `#C58C94` exact on all 5 applicable pages |
| Reference divider coverage | ✓ (post-fix) | p24 divider restored (was erased by shift) |
| Abstract box uniformity | ✓ | 5/5 article first pages use identical `#FEF8F8` + `#D8B4B9` scheme |
| Corner triangle uniformity | ✓ | 5/5 article first pages: 14 pt, `#8B1A2B` |
| Rule width uniformity | ✓ | Header rules 0.298 pt, frontmatter rules 0.597 pt, triangles 1.0 pt |

## Pass 1 · Ornament inventory by type

### 1. Cover backgrounds (pp 1, 34)

| Element | Color | Dimensions |
|---|---|---|
| Outer fill | `#131313` charcoal | full page |
| Inner fill (10 mm inset) | `#1F1F1F` | 28,28 → 584,764 |
| Frame line | `#C9B38A` beige | 0.498 pt stroke |
| Accent separator | `#C9B38A` | 0.398 pt |

Applied to Portada (p1) and Contraportada (p34). Consistent framing across both covers.

### 2. Institutional burgundy rules

Used as signature accent throughout the volume.

| Zone | y | Width (pt) | Stroke (pt) |
|---|---|---|---|
| Frontmatter header (pp 3-6, 32-33) | 71 | 510 | 0.597 |
| Frontmatter footer (pp 3-6, 32-33) | 717.5 | 510 | 0.597 |
| Article body header (all article pp) | 49 | 498.6 | 0.298 |
| Article first footer (p7, p10, p13, p20) | 750.9 | 498.6 | 0.298 or 0.4 |
| Article first footer (p25) | 762 | 498.6 | 0.4 |
| Table 1 rules (p28) | 69, 96 | 498.6 | 0.8, 0.5 (black, not burgundy) |

All burgundy rules now render as exact `#8B1A2B` after the color normalization fix (`BURGUNDY = (0x8B/255, 0x1A/255, 0x2B/255)` in `rapm_config.py`).

### 3. Abstract boxes (article first pages)

Present on pp 7, 10, 13, 20, 25. Identical structure:

- Fill: `#FEF8F8` pale rose
- Top burgundy rule: `#8B1A2B`, 0.298 pt
- Left and right vertical brackets: `#D8B4B9` light pink, 0.398 pt, 8 segments (decorative)
- Width: 498 pt spanning text area
- Height: varies by abstract length

### 4. Corner triangles (article first pages)

Top-right corner ornament on pp 7, 10, 13, 20, 25.

- Size: 14 pt equilateral
- Fill: `#8B1A2B` burgundy
- Position: bbox [598, 0, 612, 14]
- Stroke width: 1.0 pt (closed polygon)

Post-fix: all 5 triangles render as exact `#8B1A2B` (previously drifted to `#8A1A2B` due to float precision).

### 5. Reference dividers (pink hairlines before "How to cite")

Light-pink separator between article body and the closing "How to cite this article" block on article last pages.

| Page | y | x-range | Width (pt) | Color |
|---|---|---|---|---|
| p9 (Editorial last) | 353 | 315–555 | 0.248 | `#C58C94` |
| p12 (Review last) | 335 | 315–555 | 0.248 | `#C58C94` |
| p19 (Recs last) | 392 | 315–555 | 0.248 | `#C58C94` |
| **p24 (Orig 1 last)** | **340** | **315–555** | **0.248** | **`#C58C94`** ← restored this pass |
| p31 (Orig 2 last) | 328 | 315–555 | 0.248 | `#C58C94` |

**Fix applied this pass**: p24 had lost its divider due to the right-column `_shift_region_clean` in phase 2.7 erasing it. Baseline v8 had it at y=364.9; after the shift (offset −25 pt) the target is y=340. Added explicit `page.draw_line(...)` with exact `(197/255, 140/255, 148/255)` floats to guarantee `#C58C94` render.

### 6. Figure drawings

#### p15 — Figure 1 (Recomendaciones diagnostic grid)

40 drawings: the anxiety-disorder severity 2×2 grid.
- Fills: `#F2D2D6` and `#F3C8CC` (pink shades for quadrants)
- Lines: `#8B1A2B` burgundy (grid + axes + arrowheads)
- All elements within the article, not header/footer ornaments

#### p22 — Figure 2 (Capacitación line chart)

75 drawings: multi-series line graph with legend.
- 5 data series colors: `#9E2433` red, `#2C5F81` blue, `#D87E2B` orange, `#3F8A4D` green, `#5B5B5B` gray
- Light gridlines in `#E7E7E7`
- Axis in `#666666` midgray

### 7. Table rules (p28 — Table 1 of the ICU-PP article)

Standard APA 7 / booktabs rules:
- Top rule: `#000000` 0.8 pt at y=69
- Header rule: `#000000` 0.5 pt at y=96
- Intermediate rules: `#2D2D2D` 0.5 pt at y=448 (3 segments)

Black (not burgundy) matches APA table convention.

### 8. White redaction rectangles

Every article body page has a white-on-white rect at `[40, 756, 580, 778]` and every frontmatter/Guides page has one at `[40, 720, 580, 740]`. These are leftover redaction artifacts from the v8 baseline that sit behind the footer text. Invisible (white on white) and non-disruptive.

### 9. Inherited Guides duplicates (pp 32-33)

Duplicate header rule at y=36 + partial content rect [0, 165, 612, 715] inherited from v8 baseline. Invisible in render; catalogued as known non-issue.

## Fixes applied this pass

### Fix 1 — Burgundy color normalization

**Problem**: Python-drawn ornaments (triangles, p13/p25 footer rules) rendered as `#8A1A2B`; LaTeX-compiled rules rendered as `#8B192B`. Visually indistinguishable (Δ1 per channel) but audit-visible.

**Root cause**: `BURGUNDY = (0.545, 0.102, 0.169)` in `rapm_config.py` — fitz truncates `0.545 × 255 = 138.975` to 138 → `#8A`, while LaTeX's `\definecolor{burg}{HTML}{8B1A2B}` specifies exact 139.

**Fix** in `rapm_config.py`:

```python
BURGUNDY   = (0x8B/255, 0x1A/255, 0x2B/255)   # exact #8B1A2B
DARKGRAY   = (0x2D/255, 0x2D/255, 0x2D/255)   # exact #2D2D2D
MIDGRAY    = (0x66/255, 0x66/255, 0x66/255)   # exact #666666
LIGHTGRAY  = (0xB2/255, 0xB2/255, 0xB2/255)   # exact #B2B2B2
HLINE_GRAY = (0xD8/255, 0xD8/255, 0xD8/255)   # exact #D8D8D8
```

Pattern: all palette constants derived from hex, not decimal approximations.

**Verification**: all 5 corner triangles + both p13 and p25 footer rules now render as exact `#8B1A2B` ✓.

### Fix 2 — p24 reference divider restored

**Problem**: p24 "How to cite this article" block had no separator line above it, while the equivalent blocks on p12, p31 (and semantically-similar regions on p9, p19) had one.

**Root cause**: `_shift_region_clean(p24, …, y_offset=-25)` in pipeline phase 2.7 correctly shifted the right-column references up, but the pixmap/text redraw path doesn't carry over the drawing primitives from the source. Ornament lines aren't in the text span extraction, so they got dropped.

**Fix** in `pipeline_rapm_v6n1.py`:

```python
p24.draw_line(fitz.Point(314.5, 340),
              fitz.Point(555.0, 340),
              color=(197/255, 140/255, 148/255),  # exact #C58C94
              width=0.248)
```

y=340 chosen to be ~12 pt above the "How to cite" text at y=352, matching the spacing on p31.

**Verification**: divider now appears at y=340 with exact `#C58C94` color. Visually confirmed on rendered p24.

## Build metadata

- Volume MD5 after fixes: `8ed6ff1df6d6609b89a90c20ba48880e`
- File size: 4,647,451 bytes (4.43 MB)
- QA: **27/27 passed** post-fix
- All 5 article first pages render identical triangle + abstract-box styling
- All 5 article last pages now have `#C58C94` reference divider (p24 restored)

## Palette registry (post-fix)

Exact hex values used in the volume, cross-language synchronized:

| Color | Hex | Python constant | LaTeX constant | Usage |
|---|---|---|---|---|
| Burgundy | `#8B1A2B` | `BURGUNDY` | `burg` | Institutional rules, triangles, H2 headers |
| Dark gray | `#2D2D2D` | `DARKGRAY` | `charcoal` | Body text |
| Mid gray | `#666666` | `MIDGRAY` | `midgray` | Captions, footer meta |
| Light gray | `#B2B2B2` | `LIGHTGRAY` | — | Portadilla dividing rule |
| Hairline gray | `#D8D8D8` | `HLINE_GRAY` | `lightgray` | Subtle separators |
| Pale rose | `#FEF8F8` | (fitz direct) | `palerose` | Abstract box fill |
| Rose accent | `#D8B4B9` | (fitz direct) | (inline) | Abstract box brackets |
| Pink hairline | `#C58C94` | (fitz direct) | (inline) | Reference divider |
| Link blue | `#1A5276` | — | `link` | DOIs, URLs |
| Beige | `#C9B38A` | — | `beige` | Cover frames |
| Cream | `#F5EEDD` | — | `cream` | Cover text |
| Cover charcoal | `#131313` | — | `bgouter` | Cover background |

12 institutional colors. All burgundy renders cross-system consistent post-fix.
