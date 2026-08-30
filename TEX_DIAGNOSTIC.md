# RAPM LaTeX Sources · Diagnostic Report

Forensic analysis of the 3 canonical LaTeX sources that drive the RAPM Vol. 6 No. 1 build chain. Metrics captured on 2026-04-19.

## 1. Inventory

| File | Lines | Bytes | Role |
|------|-------|-------|------|
| `RAPM_VOL6_NO1_Portada_v7.tex` | 226 | 9,487 | Front cover (LX anniversary) |
| `RAPM_VOL6_NO1_Contraportada_v3.tex` | 162 | 8,352 | Back cover (logo + QR) |
| `Informe_Cierre_Editorial_V6N1.tex` | 270 | 15,380 | Editorial closure report |

## 2. Critical findings (BLOCKING reproducibility)

### CRIT-1 · `texlive-lang-spanish` not installed in current environment
All three sources use:
```latex
\usepackage[english,spanish,es-tabla,es-nodecimaldot]{babel}
```
These options require the `spanish.ldf` locale file, which ships in `texlive-lang-spanish`. In the current container only `babel-es-MX.ini` / `babel-spanish-mexico.tex` are available — **not enough**. All three files fail to compile with:
```
Package babel Error: Unknown option 'spanish'.
```
**Fix:** `apt-get install texlive-lang-spanish` — or migrate to modern babel:
```latex
\usepackage[main=spanish,english]{babel}
\babelprovide[import]{spanish-mexico}
```

### CRIT-2 · `portada_oleo_vignette.jpg` missing
The Portada v7 references the Der Psychiater oil painting:
```latex
\includegraphics[height=200mm,keepaspectratio]{portada_oleo_vignette.jpg}
```
This JPG was swept away by the cleanup `rm *.jpg` command. The compiled `Portada_v7.pdf` still exists and the build chain (`pipeline_rapm_v6n1.py`) does not recompile it — but **the .tex cannot rebuild without the image**.

**Fix:** Restore from project backup, extract from compiled PDF, or regenerate from the original painting.

## 3. High-severity issues

### HIGH-1 · Deprecated babel options
```
[english,spanish,es-tabla,es-nodecimaldot]
```
Modern babel (>= 3.42) loads Spanish via `\babelprovide[import]{spanish-mexico}` and exposes locale options through `\babelsetup` / `\babelfont`. The legacy option names are retained only through the compatibility shim and emit no warning until the `.ldf` file is absent (then hard-fail).

### HIGH-2 · Positional fragility (covers only)
| File | `textblock` positions | `\fontsize{}{}\selectfont` chains |
|------|----------------------|-----------------------------------|
| Portada v7 | **22** hardcoded (x, y) | **39** |
| Contraportada v3 | **20** | **17** |
| Informe | 0 (normal flow) | 16 |

The covers are essentially hand-placed layouts via `textpos`. Any change to page geometry propagates across dozens of coordinates. Mitigation: extract `y` coordinates to `\newcommand{\yTitle}{22}`, `\newcommand{\yLogo}{53}` etc. — a 5-minute refactor that makes future edits safe.

### HIGH-3 · No semantic heading markup
All three sources use pure visual positioning (textblocks + sized spans). None calls `\section`, `\subsection`, `\subsubsection`. Impact:
- PDF is not *structured* (no logical tree)
- Screen readers cannot navigate
- No automatic outline beyond what hyperref injects
- Fails WCAG 2.1 AA §1.3.1 (info and relationships)

The project specification in `userMemories` requires WCAG 2.1 AA — covers and closure report are exempt in practice, but the lack of structure compounds CRIT-3 below.

## 4. Medium-severity issues

### MED-1 · Mixed accent styles
| File | Unicode chars (`á é í`) | Backslash escapes (`\'a \'e \'i`) |
|------|--------|------------------|
| Portada v7 | 8 | 28 |
| Contraportada v3 | 7 | 9 |
| Informe | 0 | ~60 |

Two different accent styles within the same file is technically fine but makes search-and-replace harder and can produce unpredictable kerning if the font has different Type 1 encodings for the escaped vs composed form. **Recommendation:** pick one. For UTF-8-native pdflatex builds, prefer Unicode.

### MED-2 · 12 packages loaded redundantly × 3 files
`geometry`, `fontenc`, `inputenc`, `babel`, `mathptmx`, `helvet`, `xcolor`, `textpos`, `tikz`, `graphicx`, `microtype`, `hyperref` — identical preamble in all three. Should be factored to a shared `rapm-editorial.cls` or `rapm-common.sty`. (The `userMemories` reference a 583-line `apm-editorial.cls` that's not present in this working dir — that's where this factoring should live.)

### MED-3 · Accessibility gaps
| Check | Portada | Contraportada | Informe |
|-------|---------|--------|---------|
| PDF `/Lang` set | ✗ | ✗ | ✗ |
| Alt text for images | ✗ | ✗ | n/a |
| `\section` semantic markup | ✗ | ✗ | ✗ |
| `\pdfmanagement-testphase` (tagged PDF) | ✗ | ✗ | ✗ |

The compiled PDFs lack the `/Lang` attribute. In the Python-side metadata pass (`pipeline_rapm_v6n1.py` → `phase3_metadata`) the XMP `dc:language = ['es', 'en']` is set, but the PDF structure itself doesn't expose `/Lang`. Adding `\hypersetup{pdflang=es-MX}` in all three would fix this with zero visual impact.

### MED-4 · `\usepackage[utf8]{inputenc}` deprecated
Since LaTeX 2018-04, UTF-8 is the default input encoding for pdflatex. The explicit declaration is harmless but clutters the preamble and may conflict with future engines. Safe to remove.

### MED-5 · Colors redefined per-file (no shared palette)
Both covers define:
```latex
\definecolor{bgouter}{HTML}{141414}
\definecolor{bginner}{HTML}{1F1F1F}
\definecolor{cream}{HTML}{F5EEDD}
\definecolor{beige}{HTML}{C9B38A}
\definecolor{muted}{HTML}{8A7F6B}
\definecolor{rose}{HTML}{D49AA5}
```
Informe defines a *different* set:
```latex
\definecolor{burg}{HTML}{8B1A2B}
\definecolor{charcoal}{HTML}{2D2D2D}
\definecolor{midgray}{HTML}{666666}
\definecolor{lightgray}{HTML}{E8E8E8}
\definecolor{palerose}{HTML}{FDF2F2}
\definecolor{link}{HTML}{1A5276}
```
- Portada/Contraportada are consistent with each other (dark theme).
- Informe palette is the *institutional* RAPM palette.
- Informe `burg` `#8B1A2B` matches exactly Python-side `BURGUNDY` in `rapm_config.py` ✓
- Could be unified into a single `rapm-colors.sty`.

## 5. Low-severity issues

### LOW-1 · Magic year strings
`2026` appears 7× in Portada, 10× in Informe as literal strings.
```latex
{\fontsize{7pt}{8.5pt}\selectfont\sffamily\color{muted}%
  Enero\textendash Abril\, /\, January\textendash April\, 2026\par}
```
**Fix:** `\newcommand{\RAPMyear}{2026}` at top, then `\RAPMyear` throughout. Cheap insurance for Vol. 7.

### LOW-2 · Informe `\noindent` × 16
Suggests structural issue — probably using manual paragraph breaks where `\parindent=0pt` globally would be cleaner. Not a real bug but indicates the document evolved organically rather than being designed.

### LOW-3 · Informe legacy em-dash `---` × 19
Typographically correct LaTeX convention, renders as U+2014. Not an error — just flag for style consistency (covers use `\textemdash` which is equivalent).

### LOW-4 · No `\hypersetup` in Contraportada
Portada and Informe set PDF metadata (pdftitle, pdfauthor, etc). Contraportada sets only pdftitle and pdfauthor. Minor asymmetry.

## 6. Good practices observed

- Consistent palette use within each file (no inline `\color[HTML]{...}`)
- `microtype` loaded everywhere for better justification
- `textpos` with explicit `\TPGrid` in mm (deterministic)
- `\TPHorizModule`/`\TPVertModule` set to 1mm (readable coordinates)
- Portada/Contraportada use identical color definitions (intentional consistency)
- Informe's palette matches `rapm_config.py` Python values exactly
- Portada sets comprehensive `\hypersetup` with pdftitle, pdfauthor, pdfsubject, pdfkeywords
- Informe uses proper `\textemdash` / `\textendash` / `\textquotedblleft` (typographically correct)
- No `\begin{center}...\end{center}` abuse (uses `\centering` where needed)
- Portada filename is the image variable (`keepaspectratio`, explicit `height=200mm`)
- Uses `\textls[100]` for proper small-caps letter-spacing
- `\color{beige}\frame{...}` around the painting — clean, composable

## 7. Reproducibility verdict

| | Compiled PDF exists | .tex recompiles |
|---|---|---|
| Portada v7 | ✓ | ✗ (missing babel-spanish, missing JPG) |
| Contraportada v3 | ✓ | ✗ (missing babel-spanish) |
| Informe | ✓ | ✗ (missing babel-spanish) |

The `pipeline_rapm_v6n1.py` build runs the Python surgery over **already-compiled** PDFs, so the current end-to-end is still ✓ functional. But touching any `.tex` source requires first restoring `texlive-lang-spanish` + the Portada image.

## 8. Overall health score

| Dimension | Score | Note |
|---|---|---|
| Compilation (right now) | ✗ 0/10 | 3/3 fail in current env |
| Compilation (with deps) | ✓ 10/10 | Compiles cleanly per earlier sessions |
| Modernity | ⚠ 5/10 | Deprecated babel options, inputenc utf8 |
| Accessibility | ⚠ 3/10 | No `/Lang`, no alt text, no `\section` |
| Semantic markup | ⚠ 4/10 | Pure visual positioning on covers |
| Maintainability | ⚠ 4/10 | Magic numbers, redundant preambles |
| Consistency (cross-file) | ✓ 7/10 | Covers match each other; Informe matches Python |
| Good practices | ✓ 8/10 | Microtype, textpos, typographic chars |

**Summary:** The `.tex` sources produce excellent output (verified by `qa_validate.py` 27/27) but are **brittle** — positional, deprecated, and dependent on environment packages not captured in the repo. The *compiled* artifacts are solid; the *source layer* is the weak link.

## 9. Prioritized fix list

1. **Restore reproducibility**: install `texlive-lang-spanish` + restore `portada_oleo_vignette.jpg`.
2. **Migrate babel options** to the modern form (or document the required TeX Live version explicitly in README).
3. **Add `\hypersetup{pdflang=es-MX}`** to all three (1-line fix, major a11y gain).
4. **Extract year to `\RAPMyear` macro** (1 minute, Vol. 7 will thank you).
5. **Factor common preamble** to `rapm-editorial.cls` (matches `userMemories` expectation).
6. **Extract cover textblock y-positions** to named macros.
7. **Add alt text** via `\hyperref` PDF string fields for the 3 images.
8. **Unify accent style** to pure Unicode (or pure `\'` — not mixed).
