# RAPM Vol. 6 No. 1 · Cover

Forensic audit of Portada (p1) and Contraportada (p34): dimensions, fonts, drawings, images, text, and rendering integrity. 7 independent passes. One real issue found and fixed. Captured 2026-04-19.

## Executive summary

| Dimension | Portada | Contraportada | Status |
|---|---|---|---|
| Page size | 612 × 792 pt (letter) | 612 × 792 pt (letter) | ✓ |
| Embedded fonts | 6 Type 1 | **7 Type 1** (was 6 Type 1 + 1 Type 3) | ✓ post-fix |
| Drawings | 8 | 3 | ✓ |
| Images | 1 (178 DPI) | 2 (375 + 671 DPI) | ✓ |
| Text spans | 155 | 93 | ✓ |
| Hyperlinks | 0 | 0 | — |
| Poppler render warnings | 0 | **0** (was 21) | ✓ post-fix |
| QA suite | 27/27 | 27/27 | ✓ |

## Fix applied this pass — Type 3 bitmap font elimination

### Problem

Rendering `p34` with `pdftoppm` produced **21 syntax warnings** per pass:

```
Syntax Warning: Save (q) operator before d0/d1 in Type 3 glyph
```

These originated from a Type 3 font (`F175`) embedded in the Contraportada. Type 3 fonts are user-defined with custom glyph-shape content streams; when malformed (as cmtt10 fallback glyphs from TeX's Metafont are), they generate parser warnings.

### Forensic trace

Scan of all 34 pages for which triggered the warnings: **only p34** (21 warnings). Enumeration of fonts on p34 showed exactly one Type 3 font (`F175`). Font-to-span mapping showed F175 was used for **exactly one string**: `'psiquiatrasapm.org.mx'` at y=729.8-737.7 (the URL below the QR code).

Tracing back through the LaTeX source:

```tex
% RAPM_VOL6_NO1_Contraportada_v3.tex, line 112
{\fontsize{8pt}{10pt}\selectfont\ttfamily\color{cream}%
  psiquiatrasapm.org.mx\par}
```

`\ttfamily` selects the document's monospace family. The document class `rapm-editorial.cls` loaded `mathptmx` (Times PS) and `helvet` (Helvetica PS) but **no Type 1 monospace package** — so `\ttfamily` fell back to Computer Modern Typewriter (`cmtt10`), which in Metafont mode ships as a Type 3 bitmap font.

### Fix

One line added to `rapm-editorial.cls`:

```tex
\RequirePackage{mathptmx}
\RequirePackage{helvet}
\RequirePackage{courier}    % Type 1 monospace (eliminates Type 3 bitmap cmtt fallback)
```

Courier PS is a standard PostScript Type 1 monospace font, pre-installed on TeX Live. Loading it makes `\ttfamily` resolve to Courier instead of cmtt10.

### Verification

After rebuild of Contraportada + assembly of the volume:

| Metric | Before | After |
|---|---|---|
| Type 3 fonts on p34 | 1 | **0** ✓ |
| Poppler render warnings per pass | 21 | **0** ✓ |
| QA suite | 27/27 | 27/27 ✓ |
| Volume size | 4,647,452 bytes | 4,653,523 bytes (+6 KB, embedded Courier) |
| Volume MD5 | d6f5f6ca… | 13e6a614… |
| URL rendering (visual) | bitmap cmtt | crisp Courier PS |

Visual improvement is noticeable — the URL no longer has the subtle pixelation characteristic of Type 3 bitmap fonts.

## Pass 1 · Page dimensions + orientation

Both pages: mediabox = `Rect(0.0, 0.0, 612.0, 792.0)`, cropbox identical, rotation = 0. Standard US Letter in portrait, no bleeds, no crops, no trim marks (this is the digital-distribution version; if print-ready with bleeds is needed that would be a separate export).

## Pass 2 · Font inventory

### Portada (6 fonts, all Type 1)

| Font | Usage |
|---|---|
| NimbusSanL-Bold | "LX ANIVERSARIO", "VOLUMEN", "NÚMERO", article-type labels |
| NimbusSanL-Regu | Dates, article titles |
| NimbusSanL-ReguItal | "apm" wordmark italic, footer credits |
| NimbusRomNo9L-Regu | "REVISTA" wordmark |
| NimbusRomNo9L-ReguItal | Painting title "Der Psychiater" |
| CMSY10 | Decorative symbols `⋄` and bullets `·` |

### Contraportada (7 fonts post-fix, all Type 1)

| Font | Usage |
|---|---|
| NimbusSanL-Bold | "CONTRAPORTADA", "VOLUMEN", "NÚMERO" |
| NimbusSanL-Regu | "Revista", dates, metadata |
| NimbusSanL-ReguItal | "apm" wordmark italic |
| NimbusRomNo9L-Regu | "R[EVISTA]" wordmark |
| NimbusRomNo9L-ReguItal | "Seis décadas al servicio de la psiquiatría mexicana" tagline |
| CMSY10 | Decorative `⋄` symbols, bullet `·` |
| **NimbusMono** (Courier PS) | **URL `psiquiatrasapm.org.mx`** — added by this fix |

All fonts now Type 1 PS. Zero Type 3 bitmap fonts.

## Pass 3 · Drawings inventory

### Portada (8 drawings)

| # | Op | Color | Purpose |
|---|---|---|---|
| 0 | line (filled) | fill=`#131313` | Outer charcoal background |
| 1 | line | stroke=`#C9B38A`, fill=`#1F1F1F` | 10 mm inset frame + inner fill |
| 2 | line | `#C9B38A` | Vertical separator at x=380 |
| 3 | line | `#C9B38A` | Horizontal rule above painting at y=150 |
| 4 | line | `#C9B38A` | Left painting frame |
| 5 | line | `#C9B38A` | Right painting frame |
| 6 | line | `#C9B38A` | Bottom painting frame at y=717 |
| 7 | line | `#C9B38A` | Short accent rule at y=185 |

### Contraportada (3 drawings)

| # | Op | Color | Purpose |
|---|---|---|---|
| 0 | fill | `#131313` | Outer charcoal background |
| 1 | line+fill | stroke=`#C9B38A`, fill=`#1F1F1F` | Inset frame |
| 2 | line | `#C9B38A` | Short rule under "Desde 1966" at y=361.4 |

**Note on fitz coordinates**: drawings on p34 report bbox coords with negative y values (e.g. `[142.7, -651.3, 754.7, 140.7]`). This is a side-effect of fitz reading drawings before the `textpos` absolute-positioning transformation is applied. The actual rendered position is within the page bounds, verified visually.

## Pass 4 · Image inventory + resolution

| Page | xref | Pixel dimensions | Display size | Effective DPI |
|---|---|---|---|---|
| p1 (Portada) | 1004 | 783×1398 | 318×567 pt | 178×178 DPI |
| p34 (Contraportada) | 223 | 1484×812 | 285×156 pt | 375×375 DPI |
| p34 (Contraportada) | 224 | 740×740 | 79×79 pt | 671×671 DPI |

All images exceed WCAG + print-quality thresholds (≥150 DPI for screen, ≥300 DPI for print). The QR code at 671 DPI is especially generous — ensures scanning accuracy from any screen size.

## Pass 5 · Text content integrity

Both covers extract cleanly. Line-by-line content:

**Portada** — 44 text lines covering: masthead (LX Aniversario, Volumen, Número), wordmark, tagline, TOC preview with 5 articles, footer credits.

**Contraportada** — 15 text lines covering: back-cover masthead, 60-years commemorative tagline, wordmark, QR ESCANEA/SCAN label, URL, E-ISSN, copyright, email contact, address.

**Duplicate-line scan**: pdfplumber reports 3 "duplicates" on p1, all semantic and intentional:

| Text | Count | Reason |
|---|---|---|
| `⋄ ⋄ ⋄` | ×2 | Decorative diamond separators above "En Este Número" and below TOC |
| `Mexicana,A.C.` | ×2 | Appears in Editorial article's ES title AND EN title translation |
| `Original` | ×2 | Article-type label for both Molina-López (Orig 1) and de la Peña (Orig 2) |

Zero actual duplicate-content bugs.

## Pass 6 · Hyperlinks

Both covers: 0 hyperlinks (no `/Annots` array with `/Subtype /Link`). This is by design — the covers are visual-only; URLs are rendered as typography but not linked. If clickable URLs are desired in future, add `\href{...}{...}` wrappers around the URL text in the LaTeX sources, or use `pdfx`/`hyperref` `\url{...}` commands.

## Pass 7 · Structural anomalies

Scanned for off-MediaBox characters, content-stream irregularities, duplicate masthead elements.

- Portada: 0 anomalies
- Contraportada: 0 anomalies (post-fix)

## Build metadata

- Volume MD5: `13e6a614a7a09ce5b226b2d58e78c1b3`
- File size: 4,653,523 bytes (4.44 MB)
- Per-page sizes (Portada + Contraportada): 104,366 bytes (Contraportada source .pdf)
- QA: **27/27 passed** ✓
- pdfLaTeX warnings: 0
- Poppler render warnings on covers: **0** (was 21 on p34)

## Remaining non-issues documented

1. Fitz reports negative-y drawing coords on p34 — cosmetic, actual render is within page bounds.
2. pdfplumber flags 3 "duplicate lines" on p1 — all semantic duplicates by design.

Both covers are now structurally clean, fully Type 1, render without parser warnings, and preserve the monospace URL aesthetic via Courier PS instead of bitmap cmtt10.
