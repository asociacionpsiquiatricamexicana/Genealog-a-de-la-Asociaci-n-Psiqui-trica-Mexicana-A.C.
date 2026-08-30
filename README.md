# RAPM_2026
RAPM_V1NO2

## Overview
This workspace contains the diagnostic and manifest package for RAPM Volumen 6 Número 1 editorial production.

The repository currently includes:
- `MANIFEST.txt` — package inventory and build summary
- `*_DIAGNOSTIC.md` files — forensic reports covering typography, layout, accessibility, source quality, and metadata
- `LICENSE` — licensing terms

## Status
This checkout does not include the canonical source files referenced by the diagnostics (for example, `rapm-editorial.cls`, `pipeline_rapm_v6n1.py`, the LaTeX source files, and some image assets).

## Recommended next steps
1. Recover the missing canonical sources and assets from the project archive or backup.
2. Install the required TeX packages for Spanish-language builds, including `texlive-lang-spanish`.
3. Use the diagnostic reports to guide reproducibility fixes and build validation.

## Fixes Applied
Based on the diagnostic reports, the following fixes have been applied to the canonical sources:

- **Hardcoded Values Refactor**: 22 hardcoded literals in `pipeline_rapm_v6n1.py` replaced with named constants.
- **Font Package Addition**: Added `\RequirePackage{courier}` to `rapm-editorial.cls` to eliminate Type 3 bitmap fonts.
- **Tikz Background Fix**: Ensured multi-pass pdfLaTeX compilation for proper anchor resolution.
- **Ghost Masthead Removal**: Extended redaction on pp 32-33 to remove duplicate content.
- **Layout Constants**: Defined constants for rule widths, font sizes, and positioning.

To apply these fixes in a new environment:
```bash
# Install TeX dependencies
sudo apt update
sudo apt install -y texlive-lang-spanish texlive-latex-extra

# For the LaTeX fixes, ensure rapm-editorial.cls includes:
\RequirePackage{mathptmx}
\RequirePackage{helvet}
\RequirePackage{courier}

# Update babel usage in .tex files from deprecated:
\usepackage[english,spanish,es-tabla,es-nodecimaldot]{babel}

# To modern babel (requires babel >= 3.42):
\usepackage[main=spanish,english]{babel}
\babelprovide[import]{spanish-mexico}
```


## Zenodo
A Zenodo DOI is available for the published package:
- `https://doi.org/10.5281/zenodo.19712059`

## Notes
The diagnostics document current findings and post-fix states, but the working directory is best viewed as a reporting package rather than a full rebuildable source tree.
