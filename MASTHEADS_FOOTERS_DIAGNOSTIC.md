# RAPM Vol. 6 No. 1 · Mastheads & Footers Diagnostic

Forensic inventory of running headers and footers across all 34 pages, by zone. Four independent passes: masthead content/position/font, footer content/position/font, intra-zone consistency, and separator rule placement. Captured 2026-04-19.

## Executive summary

| Dimension | Status | Notes |
|---|---|---|
| Footer content | ✓ | Uniform `Publicado por...` + `N / 34` + `CC BY-NC 4.0` on 30 interior pages |
| Footer y-position per zone | ✓ | Zero variance within each zone (all identical) |
| Masthead content per zone | ✓ | Zone-appropriate running heads, consistent within each zone |
| Masthead y-position per zone | ✓ | Zero variance within each zone (except body pages where title lines vary with article) |
| Separator rule color | ✓ (post-fix) | All article first/body pages now burgundy `#8B1A2B` |
| Separator rule position | ✓ (post-fix) | All uniform at y=750.9 except p25 (y=762, avoids Keywords collision) |
| Inherited v8 artifact | ⚠ pp 32-33 | Duplicate masthead at y=4.3 — invisible, from baseline |

## Pass 1 · Masthead inventory by zone

### Cover front (p1)

`LX ANIVERSARIO` · `VOLUMEN 6 · NÚMERO 1` · `Enero–Abril / January–April 2026` · wordmark `REVISTA apm` centered (43.8 pt Nimbus Roman). Commemorative 60th anniversary layout.

### Portadilla (p2)

No masthead band (intentional — full-page design element).

### Frontmatter (pp 3-6: Directorio, Sobre Nosotros, Mission, Comité, TOC)

All four pages share identical masthead structure at y=40-60:

- `Volumen 6, Número 1` (Palladio Bold 11pt, burgundy) — left
- `REVISTA apm` wordmark (Palladio Roman+Italic 13.9pt, burgundy) — right
- `Enero·Abril·2026` + `Asociación Psiquiátrica Mexicana, A.C.` (small Palladio 4.9-6.8pt, gray) — supplementary

**y-position: 40.2 pt on all 4 pages** ✓ zero variance.

### Article first pages (pp 7, 10, 13, 20, 25)

- `Rev Asoc Psiquiatr Mex.` (Palladio Italic 7.5pt)
- DOI URL `https://doi.org/10.5281/zenodo.XXXXXXXX`
- `apm` wordmark (Palladio Bold 15.9pt)

**y-positions uniform: 56.6 (citation), 66.3 (DOI), 67.8 (apm) across all 5 first pages** ✓

### Article body pages (20 pages: pp 8-9, 11-12, 14-19, 21-24, 26-31)

Running head at y=37.0: `Rev Asoc Psiquiatr Mex. 2026;6(1) · [Author Surname], [et al.] (2026)` (Palladio Italic 8pt).

Author surname varies per article:
- Medina-Rodríguez (pp 8-9, editorial)
- Munch-Anguiano, L., et al. (pp 11-12, review)
- Alviso de la Serna, L.D., et al. (pp 14-19, recommendations)
- Molina-López, A., et al. (pp 21-24, original 1)
- de la Peña Olvera, F.R., et al. (pp 26-31, original 2)

**y-position: 37.0 on all 20 pages** ✓ zero variance.

### Guides (pp 32-33)

Same masthead structure as frontmatter at y=39.3-57.3. **Visually identical to frontmatter.**

⚠ Duplicate stream artifact: text at y=4.3-22.3 replicates the masthead content. **Invisible in rendered output** (fitz's `get_text("dict")` doesn't see it; pdfplumber does). Verified present in v8 baseline, v16, and current — inherited from the original LaTeX compilation of the Guides section, not introduced by the pipeline. 77 characters affected per page.

### Cover back (p34)

`CONTRAPORTADA` · `VOLUMEN 6 · NÚMERO 1` · `Revista apm – Back Cover` at y=36-46 (Nimbus Sans). Back cover design.

## Pass 2 · Footer inventory by zone

### Cover front (p1)

Custom cover footer: painting title `Der Psychiater`, author credit, technical caption, e-ISSN, CC BY-NC 4.0, © 2026 APM. Spans y=730-765.

### Portadilla (p2) + Frontmatter (pp 3-6)

Unified footer at y=725-726:
- `Publicado por la Asociación Psiquiátrica Mexicana, A.C.` (Palladio Regular 8pt)
- `N / 34` centered (Palladio Regular 9pt)
- `CC BY-NC 4.0` right
- **y=726.2 on all 5 pages** ✓

### Article body pages (pp 7-31)

Unified footer at y=765:
- `Publicado por la Asociación Psiquiátrica Mexicana, A.C.` (Palladio Regular 8pt)
- `N / 34` centered
- `CC BY-NC 4.0` right
- **y=765.2 on all 25 pages** ✓ zero variance

### Guides (pp 32-33)

Same as frontmatter at y=726.2 ✓

### Cover back (p34)

Custom back cover footer: e-ISSN `3061-7979`, email `revistaapm@psiquiatrasapm.org.mx`, © 2026 APM · CC BY-NC 4.0, address. Spans y=717-746.

## Pass 3 · Separator rule consistency (post-fix)

### Pre-fix state

| Pages | Rule y | Width | Color |
|---|---|---|---|
| p7, p10, p20 | 750.9 | 498.6 pt | `#8B1A2B` burgundy |
| p13 | 762.0 | 498.3 pt | `#D8D8D8` light gray ⚠ |
| p25 | 762.0 | 498.3 pt | `#D8D8D8` light gray ⚠ |

Visual verification confirmed p13 and p25 looked lighter and tighter-to-footer than other article first pages.

### Fix applied

`pipeline_rapm_v6n1.py`, two occurrences of `draw_ornamental_hline`:

- **p13**: changed from `y=762, color=HLINE_GRAY` to `y=750.9, color=BURGUNDY, width=0.4`
- **p25**: kept y=762 (Keywords block extends to y=750.2, collision would occur at 750.9), but changed color to `BURGUNDY, width=0.4`

### Post-fix state

| Pages | Rule y | Width | Color |
|---|---|---|---|
| p7, p10, p13, p20 | 750.9 | 498.6 pt | `#8B1A2B` burgundy ✓ |
| p25 | 762 | 498.6 pt | `#8B1A2B` burgundy ✓ |

All article first pages now use uniform burgundy color. p25 position difference is design-necessitated (Keywords block).

### Other rules (unchanged)

- Frontmatter pp 3-6: header rule y=71.2, footer rule y=717.5, width 510pt, burgundy ✓
- Article body pp 8+ (except first pages): header rule y=48.6, footer rule y=750.9, burgundy ✓
- p28: extra black rule at y=69.2 (Table 1 top rule, intentional)
- p32, p33: have duplicate header rule at y=36.2 (inherited artifact, invisible)

## Pass 4 · Intra-zone consistency final verdict

| Zone | Pages | Footer y | Folio y | Masthead y | Uniformity |
|---|---|---|---|---|---|
| cover_front | 1 | 730.0 | — | — | N/A |
| portadilla | 1 | 726.2 | 725.5 | — | — |
| frontmatter | 4 | 726.2 | 725.5 | 40.2 | ✓ 4/4 |
| article_first | 5 | 765.2 | 764.5 | 56.6 | ✓ 5/5 |
| article_body | 20 | 765.2 | 764.5 | 37.0 | ✓ 20/20 |
| guides | 2 | 726.2 | 725.5 | 39.3 | ✓ 2/2 |
| cover_back | 1 | — | — | 36.4 | N/A |

**All 30 interior pages uniform within their zone.** Zero footer y-variance, zero masthead y-variance per zone.

## Build metadata

- Volume MD5 after fix: `c4b81adab9062ff7471c031e8618be6c`
- File size: 4,647,295 bytes (4.43 MB)
- QA: **27/27 passed** post-fix
- Visual parity verified on p13, p20, p25 via high-DPI re-render

## Known non-issue retained

pp 32-33 duplicate masthead at y=4.3 (77 chars per page):
- Inherited from v8 baseline LaTeX compilation of the Guides section
- Invisible in rendered output (outside PDF viewer clip)
- Not generated by the pipeline
- Fixable only by re-compiling the Guides `.tex` source (not in canonical codebase)
- Classification: structural hygiene, non-blocking
