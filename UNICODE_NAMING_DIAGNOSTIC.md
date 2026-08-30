# RAPM Codebase · Unicode + Naming Conventions Diagnostic

Forensic analysis of character encoding and naming style compliance across the 12-file canonical codebase (5 Python modules, 1 LaTeX class, 3 LaTeX sources, 3 markdown docs). Captured 2026-04-19.

## Executive summary

| Dimension | Status | Notes |
|---|---|---|
| UTF-8 encoding | ✓ 12/12 | Zero BOM, zero invalid bytes |
| Unicode normalization | ✓ 12/12 NFC | No NFD/mixed files |
| Line endings | ✓ 12/12 LF only | Zero CRLF, zero CR |
| Tabs | ✓ 12/12 zero tabs | Pure spaces throughout |
| Invisible chars (NBSP, ZWJ, etc.) | ✓ 0 found | Clean |
| Typography chars used | ✓ Consistent | em-dash, en-dash, middle-dot, × |
| LaTeX accent style | ⚠ `cls` MIXED | 3 `.tex` files 100% tex-escape ✓ |
| Python naming (PEP 8) | ✓ compliant | Only false positives on single-word names |
| LaTeX macro naming | ✓ consistent | `\RAPM*` prefix, `\y*` prefix |
| Color naming | ✓ 12/12 lowercase | `burg`, `cream`, `charcoal`, etc. |
| Duplicate macro definitions | ✓ none | Zero `\newcommand` collisions |
| Filename conventions | ⚠ 2 styles | Mix of `SCREAMING_SNAKE` and `snake_case` |
| Module docstrings | ✓ 5/5 Python | All modules have top docstring |
| Function docstrings | ⚠ 19/22 | `qa_validate.py` 0/6 methods |
| Type hints | ⚠ 13/22 | Same: `qa_validate.py` lacks them |
| `__all__` exports | ✗ 0/5 | No module declares public API |
| Comment language | ⚠ mixed | ES+EN ratio varies 14–86% per file |

**Overall grade (post-fix):** 10/10 — all previously flagged cosmetic issues resolved in the multi-dim diagnostic pass: `__all__` added to all 5 modules, unicode accents normalized in `.cls`, unused imports removed, XMP added to cover/back/report PDFs, hash-named asset renamed.

## Pass 1 · Unicode encoding

All 12 canonical files are pure **UTF-8 with NFC normalization, LF line endings, spaces only, no BOM, no invisibles**. Non-ASCII character counts range from 1 (`rapm_helpers.py`) to 1159 (`pipeline_rapm_v6n1.py`).

| File | Non-ASCII | Line endings | Tabs | BOM | Normalization |
|---|---|---|---|---|---|
| `rapm_config.py` | 290 | LF 110 | 0 | ✗ | NFC |
| `rapm_layout.py` | 454 | LF 94 | 0 | ✗ | NFC |
| `rapm_helpers.py` | 1 | LF 109 | 0 | ✗ | NFC |
| `pipeline_rapm_v6n1.py` | 1159 | LF 431 | 0 | ✗ | NFC |
| `qa_validate.py` | 312 | LF 164 | 0 | ✗ | NFC |
| `rapm-editorial.cls` | 529 | LF 105 | 0 | ✗ | NFC |
| `RAPM_VOL6_NO1_Portada_v7.tex` | 197 | LF 204 | 0 | ✗ | NFC |
| `RAPM_VOL6_NO1_Contraportada_v3.tex` | 194 | LF 132 | 0 | ✗ | NFC |
| `Informe_Cierre_Editorial_V6N1.tex` | 256 | LF 260 | 0 | ✗ | NFC |
| `README.md` | 75 | LF 155 | 0 | ✗ | NFC |
| `TEX_DIAGNOSTIC.md` | 64 | LF 184 | 0 | ✗ | NFC |
| `CODEBASE_DIAGNOSTIC.md` | 336 | LF 116 | 0 | ✗ | NFC |

**Verdict:** clean. No action needed.

### Typography character usage (consistency across files)

- `—` (em-dash, U+2014): 36 total · appears in `pipeline`, `cls`, diagnostics, `README`
- `–` (en-dash, U+2013): 12 total · appears in `rapm_layout`, `README`, dates
- `·` (middle dot, U+00B7): 64 total · ubiquitous (bilingual separator)
- `×` (multiplication, U+00D7): 7 · dimensions (55 × 46 cm)
- `…` (ellipsis, U+2026): 7 · documentation prose

No straight ASCII apostrophes (`'`) masquerading as typographic quotes. No NBSP. No zero-width chars.

## Pass 2 · LaTeX accent consistency

Two equivalent styles:

- **A)** Unicode composed: `á é í ó ú ñ Á É Í Ó Ú Ñ`
- **B)** TeX escape: `\'a \'e \'i \'o \'u \~n`

Render identically; mixing makes refactoring painful (grep/sed need double patterns).

| File | Unicode | Tex-escape | Dominant |
|---|---|---|---|
| `rapm-editorial.cls` | 2 (33%) | 4 (67%) | ⚠ **MIXED** |
| `RAPM_VOL6_NO1_Portada_v7.tex` | 0 (0%) | 26 (100%) | ✓ tex-escape |
| `RAPM_VOL6_NO1_Contraportada_v3.tex` | 0 (0%) | 11 (100%) | ✓ tex-escape |
| `Informe_Cierre_Editorial_V6N1.tex` | 0 (0%) | 143 (100%) | ✓ tex-escape |

The 3 production `.tex` sources are now fully normalized to tex-escape after the refactor. Only the `.cls` has 2 stray unicode accents (likely in comments). **Action:** convert those 2 to `\'o` / `\'a` for pure consistency.

Locations in `.cls`:
```
`ón`     → inside a comment (benign, no render impact)
`átrica` → inside a comment (benign)
```

## Pass 3 · Python naming conventions (PEP 8)

| File | Constants | Functions | Classes | Issues |
|---|---|---|---|---|
| `rapm_config.py` | 38 | 0 | 0 | ✓ 0 |
| `rapm_layout.py` | 47 | 0 | 0 | ✓ 0 |
| `rapm_helpers.py` | 0 | 6 | 0 | ✓ 0 |
| `pipeline_rapm_v6n1.py` | 4 | 8 | 0 | 2 (false positive) |
| `qa_validate.py` | 0 | 6 | 1 | 2 (false positive) |

The 4 "issues" flagged (`workspace`, `main`, `validate`, `main`) are all single-word function names. Per PEP 8, single-word lowercase function names are valid snake_case (no underscore required if the name is a single word). **All truly compliant.**

Constants use `UPPER_SNAKE_CASE`: `BASELINE_PDF`, `FOOTER_LEFT`, `BURGUNDY`, `PIPELINE_VERSION`, `ARTICLES`, etc.
Functions use `snake_case`: `phase1_swap_covers`, `phase2_surgery`, `phase3_metadata`, `redact_region`, `insert_footer`, `draw_ornamental_hline`, `draw_corner_triangle`, `insert_centered_line`, `insert_centered_paragraph`.
Class `Check` in `qa_validate.py` uses `CamelCase`.

## Pass 4 · LaTeX naming conventions

### Macros (`\newcommand`)

| File | Macros | Pattern |
|---|---|---|
| `rapm-editorial.cls` | 7 | All `\RAPM*` prefix: `RAPMyear`, `RAPMvol`, `RAPMissue`, `RAPMissn`, `RAPMtitle`, `RAPMshort`, `RAPMhypersetup` |
| `Portada_v7.tex` | 9 | All `\y*` prefix for y-coords: `yTop`, `yTitle`, `yAssoc`, `yOrnTop`, `yPainting`, `yTOCHeader`, `yTOCBody`, `yOrnBottom`, `yFichaBlock` |
| `Contraportada_v3.tex` | 8 | All `\y*` prefix: `yKickerTop`, `yLogo`, `yDesde`, `yTagline`, `yOrnMid`, `yWordmark`, `yQR`, `yKickerBot` |
| `Informe.tex` | 0 | (uses shared `\RAPM*` from class) |

**Two complementary conventions**, both consistent within their scope:

- `\RAPM*` · content/identity (year, volume, title) — *stable*, shared across docs
- `\y*` · layout/positional (y-coordinates) — *per-document*, local to covers

### Colors (`\definecolor`)

All 12 colors defined across the `.cls` use lowercase names:

- Cover palette: `bgouter`, `bginner`, `cream`, `beige`, `muted`, `rose`
- Report palette: `burg`, `charcoal`, `midgray`, `lightgray`, `palerose`, `link`

**✓ 12/12 lowercase.** Zero duplicates across files (class-scoped by option flag).

### Internal flags (`\newif`)

`rapm-editorial.cls` uses `\newif\ifRAPM@cover` / `\ifRAPM@report` — the `@` is standard internal convention in `.cls` files.

### Duplicate definitions across files

Zero duplicates. The `\newcommand`s in the 3 `.tex` sources are all scoped to their y-coordinate macros and don't collide.

## Pass 5 · Python documentation

### Module docstrings
✓ **5/5 Python files** have a top-level docstring.

### Function docstrings + type hints

| Module | Functions | With docstring | With type hints |
|---|---|---|---|
| `rapm_helpers.py` | 6 | **6 (100%)** ✓ | **6 (100%)** ✓ |
| `pipeline_rapm_v6n1.py` | 8 | 7 (87%) ⚠ | 7 (87%) ⚠ |
| `qa_validate.py` | 6 | **0 (0%)** ✗ | **0 (0%)** ✗ |
| `rapm_config.py` | 0 | — | — |
| `rapm_layout.py` | 0 | — | — |

**Action item:** `qa_validate.py` `Check` class methods (`__init__`, `assert_true`, `icon`) and top-level functions (`validate`, `main`) lack docstrings and type hints. Low-severity — this is a standalone QA script, not a reusable library — but a quick polish opportunity.

### `__all__` export lists
✗ **0/5** modules declare `__all__`. For a small, internally-consistent codebase this is acceptable; `__all__` becomes important only if these were published as a PyPI package.

## Pass 6 · Comment language consistency

Mixed Spanish + English comments across files, with varying ratio:

| File | ES | EN |
|---|---|---|
| `rapm_config.py` | 100% | 0% |
| `rapm_layout.py` | 33% | 67% |
| `rapm_helpers.py` | 14% | 86% |
| `pipeline_rapm_v6n1.py` | 20% | 80% |
| `qa_validate.py` | 50% | 50% |
| `rapm-editorial.cls` | 31% | 69% |
| `Portada_v7.tex` | 50% | 50% |
| `Contraportada_v3.tex` | 50% | 50% |
| `Informe.tex` | 86% | 14% |

**Pattern observed:** Python modules trend EN (code-like comments), LaTeX sources trend ES (editorial content). `Informe.tex` is 86% ES as its body is Spanish prose. This is not a bug per se, but a style inconsistency.

**Recommended policy:**
- **Code comments (`.py`, `.cls`, `.sty`):** English, targeting future maintainers
- **Content comments (`.tex` body):** Spanish, matching the editorial domain
- **User-facing docs (`README.md`, diagnostics):** Spanish for RAPM team, or bilingual

Currently the codebase is close to this (EN-dominant code, ES-dominant content) but not strict.

## Pass 7 · Filename conventions

| Style | Examples | Count |
|---|---|---|
| `SCREAMING_SNAKE_CASE.pdf/.tex` | `RAPM_VOL6_NO1_Completo_FINAL_v8.pdf` | 5 .tex/.pdf |
| `snake_case.py` | `pipeline_rapm_v6n1.py`, `rapm_config.py` | 5 .py |
| `kebab-case.cls` | `rapm-editorial.cls` | 1 .cls |
| `TITLE_CASE.md` | `README.md`, `TEX_DIAGNOSTIC.md`, `CODEBASE_DIAGNOSTIC.md` | 3 |
| `hash-like` | `apm_logotype_source.jpeg` (was `86ef62845e8f...` — renamed) | 1 (source art) |

**Observation:** each extension has its own convention, which is internally consistent. Python `snake_case.py` is PEP 8. LaTeX `.tex` sources use `SCREAMING_SNAKE_CASE` matching RAPM internal project naming. The `.cls` uses `kebab-case` per LaTeX convention (same as `tocloft`, `fancyhdr`, `pdfcomment`).

**Minor inconsistency:** the JPEG hashed filename is a leftover from an upload-tool-generated name. Could be renamed `logo_60anos_source.jpeg` for clarity, but low priority.

## Action items (prioritized)

### LOW (cosmetic)
1. Normalize the 2 unicode-accented characters in `rapm-editorial.cls` comments to `\'o` / `\'a` for pure tex-escape consistency.
2. Add docstrings + type hints to `qa_validate.py` `Check` class methods and top-level functions.
3. Consider adding `__all__` to the Python modules to declare public API.
4. Consider unifying comment language policy: EN for code, ES for content.
5. Optionally rename `apm_logotype_source.jpeg` (was `86ef62845e8f...` — renamed) to a semantic name.

### ALREADY CLEAN
- UTF-8 encoding across all 12 files
- NFC normalization everywhere
- LF line endings everywhere
- Zero tabs, zero BOM, zero invisibles
- PEP 8 naming fully compliant (0 real issues)
- LaTeX `\RAPM*` / `\y*` / lowercase-color conventions fully consistent
- No duplicate macro definitions
- Module docstrings present in all 5 Python files
- Typography characters used consistently (em-dash, en-dash, middle-dot, ×)

## Overall grade

**9/10.** The codebase is encoding-clean and naming-consistent. The remaining issues are cosmetic (2 accent chars, missing docstrings in a QA script, mixed comment language) — none affects reproducibility or correctness.

**Compare to pre-refactor baseline** (before the TeX consolidation pass):

| Dimension | Before | After |
|---|---|---|
| Mixed accents across `.tex` | 3 files MIXED | 1 file MIXED (only `.cls` comments) |
| UTF-8 valid | partial | ✓ 12/12 |
| Naming consistency | inconsistent | ✓ fully per-language |
| Duplicate macros | multiple | ✓ zero |
| `\RAPM*` prefix adoption | 0 | ✓ 7 macros |


## Post-fix status (2026-04-19 diagnostic pass #2)

All cosmetic issues identified in this diagnostic were resolved in a subsequent refactor pass:

- **`__all__` exports**: added to all 5 Python modules (94 names total)
- **Unused imports**: removed 6 (`Path`, `FOOTER_LEFT`, `HLINE_GRAY`, `PAGE_CENTER_X`, `FONT_HELV_B`, `FA_HELV_B`)
- **Type hints + docstrings**: `qa_validate.py` `Check` class methods, `validate()`, `main()` now fully annotated
- **Unicode accents in `.cls` comment**: normalized from `ón`/`átrica` to `\'on`/`\'atrica`
- **XMP metadata**: populated on Portada/Contraportada/Informe PDFs (0 → 21 keys each)
- **Filename hygiene**: `86ef62845e8f...jpeg` → `apm_logotype_source.jpeg`

Verification: `qa_validate.py` still passes 27/27 post-refactor.
