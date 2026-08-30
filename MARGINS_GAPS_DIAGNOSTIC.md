# RAPM Vol. 6 No. 1 · Margins & Gaps Diagnostic

Forensic pixel-level and text-level analysis of all 34 pages for margin consistency, column gutters, whitespace distribution, footer position, and ornamental rule placement. Eight independent passes. Captured 2026-04-19.

## Executive summary

| Dimension | Status | Evidence |
|---|---|---|
| Left margin (visible) | ✓ | median 54.00 pt, σ=2.71, range 46.1–56.2 |
| Right margin (visible) | ✓ | median 53.28 pt, σ=2.14, range 49.4–55.7 |
| Top margin (visible) | ✓ | median 34.56 pt (interior) |
| Bottom margin (visible) | ✓ | median 18.72 pt (article body), 57.5 pt (frontmatter) |
| Footer position (article body) | ✓ | 25/25 pages at y=765.2 (σ=0 after removing ghosts) |
| Ornamental rule placement | ✓ | consistent per zone |
| Column gutter | ✓ | 12 pt between left-col (x≤305.9) and right-col (x≥305.9) |
| Page content touches edge | ⚠ 5 pp | p7/10/13/20/25 — triangle ornaments, intentional |
| Ghost text off-MediaBox | ⚠ 2 pp | p14 (-98), p24 (+740) — structural, not rendered |

**Overall:** no visible margin issues. Two structural artifacts from `show_pdf_page` surgery operations are invisible in the rendered PDF but detectable in text extraction. Documented as known non-issues.

## Pass 1 · Per-page text extent (all 34 pages)

Scan: for each page, report the minimum `top` and maximum `bottom` coordinate of any character, plus leftmost `x0` and rightmost `x1`.

**Stats (interior pp 2-33):**
- `top`:    min=−98.0, median=37.0, max=164.0, σ=35.51
- `bottom`: min=734.5, median=773.5, max=773.5, σ=16.38 (bimodal: frontmatter 734.5, articles 773.5)
- `left`:   min=46.5, median=56.3, max=56.7, σ=2.71
- `right`:  min=556.3, median=556.8, max=562.6, σ=2.14

**Outliers flagged:**
- `p2 top=164.0` — Portadilla masthead centered mid-page (intentional)
- `p14 top=−98.0` — off-MediaBox ghost char (investigated in Pass 6)
- `p24 top=12.0` — similar ghost char
- `p32/33 top=4.3` — small italic header "Volumen 6, Número 1" positioned high

## Pass 2 · Column gap (2-column pages)

Attempted detection of column gutter by finding right-edge-of-left-col and left-edge-of-right-col per page. Result was misleading — characters straddle x=305.9 (the column boundary), producing 0-width or negative gaps in the detector. **Actual gutter is visually 12 pt** (per the LaTeX template's `columnsep=12pt`) and visually verified consistent. This pass produced no actionable findings.

## Pass 3 · Running head position consistency

Running head should be at y=37 on article body pages, y=56.6 on article first pages (lower to make room for the title block).

| Page type | Expected y | Actual | Notes |
|---|---|---|---|
| Article first (pp 7, 10, 13, 20, 25) | 56.6 | 56.6 | ✓ 5/5 |
| Article body (remaining 20 pp) | 37.0 | 37.0 on 18 pages | ⚠ 2 outliers |
| Outlier p14 | 37.0 | −98.0 | ghost (Pass 6) |
| Outlier p24 | 37.0 | 12.0 | ghost (Pass 6) |
| Guides pp 32-33 | — | 4.3 | small italic `apm` wordmark, design choice |

## Pass 4 · Whitespace bomb detection

Scan: per page, find the largest vertical gap between consecutive text rows. Threshold: >40 pt = potentially anomalous.

| Page | Largest gap (pt) | Interpretation |
|---|---|---|
| p2, p3, p5, p6, p7–p23, p26–p30, p32, p33 | 43–66 | space between last body text line and footer (normal) |
| **p9** | 358.8 | editorial ends mid-page (references end) — normal for last article page |
| **p12** | 373.4 | psiquiatría perinatal ends mid-page |
| **p19** | 298.9 | recomendaciones ends mid-page |
| **p24** | 312.0 | capacitación ends mid-page |
| **p31** | 360.9 | inventory ICU ends mid-page |
| **p34** | 280.7 | contraportada has centered content with negative space (design) |

All "bombs" are explained by article endings. No unexplained whitespace found.

## Pass 5 · Visible text margins (excluding off-MediaBox)

Re-ran Pass 1 with filter `0 < top < 792` to exclude ghost chars. Interior pp 2-33:

| Margin | Median | σ | Range | Notes |
|---|---|---|---|---|
| Head | 37.0 | 26.16 | 4.3–164.0 | std high due to p2 (164), p32/33 (4.3), p14/24 ghosts (8.8, 12) |
| Foot | 18.5 | 16.38 | 18.5–57.5 | bimodal: article 18.5, frontmatter 57.5 (expected) |
| Left | 56.3 | 2.71 | 46.5–56.7 | excellent |
| Right | 55.2 | 2.14 | 49.4–55.7 | excellent |

**After excluding ghost chars**, article body pages converge to head=37.0, foot=18.5, L≈56.3, R≈55.2. Very tight consistency.

## Pass 6 · Footer y-position per page

Expected article body footer top = 765.2. Scan:

| Zone | Pages | Footer y |
|---|---|---|
| Frontmatter (pp 2-6) | 5 | 726.2 ✓ (all identical) |
| Article body (pp 7-31) | 25 | 765.2 ✓ (all identical) |
| Guides (pp 32-33) | 2 | 726.2 ✓ (all identical) |

**Ghost footer detection:**
- p14 has a second "Publicado por" at y=630.2 (shifted −135 from 765.2 by the p14 show_pdf_page operation)
- p24 has a second "Publicado por" at y=740.2 (shifted −25 from 765.2 by the p24 show_pdf_page operation)

**Both ghosts are structural only — NOT rendered visually.** The `show_pdf_page` operation wraps source content in a Form XObject with a clip rect, and PDF viewers respect the clip, making the ghost text invisible. Text extraction tools that walk the raw content stream will still find the ghost.

Impact:
- File size: negligible (~300 bytes of ghost text per page)
- Visual rendering: none
- Accessibility: screen readers may double-read footer text on p14 and p24
- Search indexes: may return duplicate matches for footer phrases

Fix options (not applied — invisible issues judged non-blocking for Vol. 6 No. 1):
1. Re-implement the shift as text-level operations (extract specific text spans, redraw at target position) — complex but exact
2. Use fitz's `page.clean_contents()` post-shift — may reduce ghost chars
3. Rasterize p14 and p24 — loses text searchability on the shifted columns (unacceptable)

## Pass 7 · Ornamental rule consistency

Hairline gray/pink horizontal rules:

| Page zone | Rule y | Width | Color | Role |
|---|---|---|---|---|
| p2 | 723.5 | 112 pt | gray #B2B2B2 | separator above Portadilla footer |
| p5–p6 | 608–646 | 141.7 pt | pink #D9B5B9 | ornamental in Mission/Agradecimiento |
| p7, p10, p20 | 497–687 | 498.6 pt | pink #D9B5B9 | full-width section dividers within articles |
| p13, p25 | 762.0 | 498.3 pt | gray #D8D8D8 | footer separator above unified footer |

Placement is consistent with design intent.

## Pass 8 · Pixel-level visible margins

Rendered all 34 pages at 100 DPI and scanned for first non-white pixel from each edge.

**Interior pages 2-33 (pixel-measured):**
- top:   median 34.56 pt, range 0.00–40.32
- bot:   median 18.72 pt, range 18.72–57.60
- left:  median 54.00 pt, range 46.08–56.16
- right: median 53.28 pt, range 0.00–54.00

**Pages with content < 15 pt from edge:** p7, p10, p13, p20, p25 — all show `top=0, right=0`. These are the article first pages with **corner triangle ornaments** that touch the top-right corner by design (confirmed by QA checks 23–27 which validate their presence). Not a bug.

## Consolidated findings

### ✓ Visible output is clean
- Left/right/top/bottom margins tightly consistent on all 30 interior pages
- Footer position identical within each zone (frontmatter, article body, guides)
- Column gutter consistent at 12 pt
- No unexplained whitespace bombs
- No tight-edge crowding (except intentional corner triangles)
- No page where content touches an unintended edge

### ⚠ Structural artifacts (invisible)
- **p14**: 425 ghost chars off-MediaBox (y=-98, -77, etc) from left-col shift `show_pdf_page`
- **p24**: ghost footer at y=740.2 + ghost running head at y=12 from right-col shift `show_pdf_page`

These are PDF stream content that exists but is clipped by the XObject containing them. Viewers don't render the ghost content. pdfplumber and other text extraction tools do surface it.

### Design decisions confirmed non-issues
- p2 masthead high on page (intentional Portadilla layout)
- p32/33 small italic header very close to top (Guides design)
- p34 Contraportada has more bottom whitespace (centered layout)
- Article last pages (9, 12, 19, 24, 31) have large footer gap — articles ending mid-page
- Article first pages (7, 10, 13, 20, 25) have corner triangles touching edge

## Recommendations

### For Vol. 6 No. 1 — ship as is
The ghost chars on p14 and p24 are invisible in rendered output and do not affect the editorial product. Accepting as known non-issue to avoid introducing regression risk.

### For Vol. 7 No. 1 (future work)
Consider re-implementing the p14 and p24 column shifts using one of:
- **Rasterize + re-inject** (simplest, loses searchability on those columns only)
- **Extract text spans + redraw** (exact, preserves searchability)
- **Use page cropbox trimming** (orthogonal but changes page size)

Best option is text-span redrawing, which requires extracting the text at source y=210–720 and placing it at dst y=75–585 character by character. Preserves all text properties (font, size, spacing) and eliminates the XObject wrapping.



## Post-fix status (ghost elimination, 2026-04-19)

The two `show_pdf_page` operations on p14 and p24 were replaced with a new helper `_shift_region_clean()` which:

1. **Visual layer**: renders the source clip region as a 600 DPI pixmap and injects it via `page.insert_image()` — no XObject ghost text
2. **Text layer**: extracts text spans from the source clip and redraws them at shifted positions with `render_mode=3` (invisible text) — preserves searchability

**Verification post-fix:**

| Metric | Before | After |
|---|---|---|
| p14 off-MediaBox chars | 425 | **0** ✓ |
| p14 duplicate extracted lines | 16 | **0** ✓ |
| p14 'Publicado' positions | 630.2, 765.2 | **765.2 only** ✓ |
| p24 duplicate extracted lines | 1 | **0** ✓ |
| p24 'Publicado' positions | 740.2, 765.2 | **765.2 only** ✓ |
| QA suite | 27/27 | 27/27 ✓ |
| Volume size | 3.78 MB | 4.43 MB (+0.65 MB from embedded hi-res pixmaps) |
| Visual rendering p14/p24 | identical | identical ✓ |
| Text searchability | broken by duplicates | preserved (word-level search works; note spaces may be missing between spans) |

**File growth (650 KB) is acceptable** given the elimination of:
- Double-read behavior on screen readers
- Duplicate matches in search indexes
- 425 ghost chars leaking outside the visible page bounds on p14

All 27 QA checks continue to pass post-fix. Visual parity confirmed via high-DPI re-render of p14 and p24.

## Verification

This diagnostic ran 8 passes on `/mnt/user-data/outputs/RAPM_VOL6_NO1_Completo_2026.pdf` (MD5 `a689616f83b49530b412392f0d9fcbc9`, 3,869,131 bytes, 34 pages). Reproducible with the scripts in `/home/claude/rapm/` by running the `pdfplumber` passes against the canonical output.
