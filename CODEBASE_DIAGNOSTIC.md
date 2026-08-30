
╔══════════════════════════════════════════════════════════════════════╗
║           CODEBASE · /home/claude/rapm                     ║
║           Project: RAPM Vol. 6 No. 1 Editorial Production             ║
╚══════════════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────────────┐
│ SECTION 1 · INVENTORY                                                 │
└──────────────────────────────────────────────────────────────────────┘

  Python pipelines:        11 files  (108 KB)
  LaTeX sources:           9 files  (portada×6, contraportada×2, informe×1)
  Completo PDFs:           17 files
  Total disk usage:        ~96 MB (debug_full/ = 5.2 MB; rest is PDFs + logs)

┌──────────────────────────────────────────────────────────────────────┐
│ SECTION 2 · CANONICAL vs LEGACY                                       │
└──────────────────────────────────────────────────────────────────────┘

  ACTIVE (keep):
    pipeline_v14.py     [canonical polish, 332 lines, 14 steps]
    pipeline_v15.py     [metadata population, 111 lines, 3 steps]
    RAPM_VOL6_NO1_Portada_v7.tex      [ref'd by v14]
    RAPM_VOL6_NO1_Contraportada_v3.tex [ref'd by v14]
    Informe_Cierre_Editorial_V6N1.tex  [standalone]
    RAPM_VOL6_NO1_Completo_FINAL_v8.pdf   [baseline — required by v14]
    RAPM_VOL6_NO1_Completo_FINAL_v14.pdf  [input for v15]
    RAPM_VOL6_NO1_Completo_FINAL_v15.pdf  [final canonical output]

  LEGACY (safe to delete, but kept for archive):
    pipeline_v2/v6/v7/v8/v9/v11/v12/v13.py  (85 KB, ~1800 lines total)
    pipeline_final.py  [vestigial from earlier session]
    integrate_volume.py [vestigial from earlier session]
    RAPM_VOL6_NO1_Portada_2026/v3/v4/v5/v6.tex  [orphan or superseded]
    Older Completo_*.pdf files  (40.3 MB reclaimable)

┌──────────────────────────────────────────────────────────────────────┐
│ SECTION 3 · CODE QUALITY FINDINGS                                     │
└──────────────────────────────────────────────────────────────────────┘

  [HIGH] pipeline_v14.py has 17 hardcoded fitz.Rect() coordinates.
         Impact: any layout change requires editing magic numbers.
         Fix: extract to a rapm_layout.py with named regions.

  [HIGH] No try/finally in any pipeline.
         Impact: WIP intermediate files leak on crash (v14_a.pdf,
         v14_b.pdf, v15_wip.pdf — they're deleted only on success).
         Fix: wrap file ops in try/finally with os.path.exists() guards.

  [MED]  Magic footer string duplicated in code.
         "Publicado por la Asociación Psiquiátrica Mexicana, A.C."
         Fix: single module-level FOOTER_LEFT constant (partially done).

  [MED]  Font paths hardcoded 3× in v14, 2× in v15.
         Fix: rapm_config.py with FONT_PATHS dict.

  [MED]  v14 and v15 must be run sequentially.
         Impact: deployment fragility.
         Fix: consolidate into pipeline_rapm_v6n1.py.

  [LOW]  No README.md / documentation.
         Impact: onboarding overhead for next session.
         Fix: README.md explaining build workflow.

  [LOW]  Integration-level tests absent.
         Impact: can't verify output regression without visual inspection.
         Fix: QA script with automated checks (already exists as one-off).

  [INFO] Missing expected files per userMemories:
         apm-editorial.cls, patch_headers.py, RAPM_SISTEMA_EDITORIAL_v2.md,
         logo_hires.png, logo_60anos.png, editorial_FINAL.tex.
         These are from separate broader RAPM system; not needed for v6 N1
         build but expected per project documentation.

┌──────────────────────────────────────────────────────────────────────┐
│ SECTION 4 · BASELINE DEPENDENCY GRAPH                                 │
└──────────────────────────────────────────────────────────────────────┘

  v8 (baseline, clean typographic homogenization)
    │
    ├─ pipeline_v9 → Completo_FINAL_v9.pdf  [ARCHIVED]
    ├─ pipeline_v11 → Completo_FINAL_v11.pdf [ARCHIVED]
    └─ pipeline_v14 → Completo_FINAL_v14.pdf [ACTIVE]
                        │
                        └─ pipeline_v15 → Completo_FINAL_v15.pdf [CANONICAL]
                                            │
                                            └─ /mnt/user-data/outputs/
                                               RAPM_VOL6_NO1_Completo_2026.pdf

  The v12, v13 pipelines operated on /mnt/user-data/outputs/ directly (mid-session
  iterations) — not part of the reproducible build chain.

┌──────────────────────────────────────────────────────────────────────┐
│ SECTION 5 · DISK USAGE ANALYSIS                                       │
└──────────────────────────────────────────────────────────────────────┘

  Reclaimable with safe cleanup:
    Legacy pipelines:       ~60 KB
    Obsolete PDFs:          ~40 MB
    Orphan TeX sources:     ~29 KB
    Debug renders:          ~5.2 MB (debug_full/, FINAL-*.jpg, v*check*.jpg)
    LaTeX aux/log files:    ~100 KB

  Total reclaimable:        ~46 MB

┌──────────────────────────────────────────────────────────────────────┐
│ SECTION 6 · RECOMMENDED CLEANUP COMMANDS                              │
└──────────────────────────────────────────────────────────────────────┘

  # Remove legacy pipelines (keep v14, v15)
  rm pipeline_v2.py pipeline_v6.py pipeline_v7.py pipeline_v8.py \
     pipeline_v9.py pipeline_v11.py pipeline_v12.py pipeline_v13.py \
     pipeline_final.py integrate_volume.py

  # Remove orphan Portada drafts (keep v7)
  rm RAPM_VOL6_NO1_Portada_2026.tex RAPM_VOL6_NO1_Portada_v3.tex \
     RAPM_VOL6_NO1_Portada_v4.tex RAPM_VOL6_NO1_Portada_v5.tex \
     RAPM_VOL6_NO1_Portada_v6.tex

  # Remove superseded Contraportada
  rm RAPM_VOL6_NO1_Contraportada_v2.tex

  # Remove legacy Completo PDFs (keep v8, v14, v15 + outputs/)
  rm RAPM_VOL6_NO1_Completo_2026.pdf \
     RAPM_VOL6_NO1_Completo_2026_FINAL.pdf \
     RAPM_VOL6_NO1_Completo_2026_final.pdf \
     RAPM_VOL6_NO1_Completo_2026_v5.pdf \
     RAPM_VOL6_NO1_Completo_FINAL.pdf \
     RAPM_VOL6_NO1_Completo_FINAL_v11.pdf \
     RAPM_VOL6_NO1_Completo_FINAL_v12.pdf \
     RAPM_VOL6_NO1_Completo_FINAL_v13.pdf \
     RAPM_VOL6_NO1_Completo_FINAL_v9.pdf \
     RAPM_VOL6_NO1_Completo_final2.pdf \
     RAPM_VOL6_NO1_Completo_shifted.pdf \
     RAPM_VOL6_NO1_Completo_v2.pdf \
     RAPM_VOL6_NO1_Completo_v3.pdf \
     RAPM_VOL6_NO1_Completo_v4.pdf

  # Remove intermediate PDFs from abandoned runs
  rm -f *_wip.pdf *_step*.pdf v*_[abc].pdf

  # Remove debug renders + LaTeX aux
  rm -rf debug_full/
  rm -f *.aux *.log *.out *.toc

┌──────────────────────────────────────────────────────────────────────┐
│ SECTION 7 · RECOMMENDED REFACTOR (optional)                           │
└──────────────────────────────────────────────────────────────────────┘

  Target architecture:

    rapm_config.py                  — constants (colors, paths, strings)
    rapm_layout.py                  — named rects (FRONTMATTER_FOOTER_Y, etc)
    rapm_helpers.py                 — redact_footer, draw_hline, insert_centered
    pipeline_rapm_v6n1.py           — single end-to-end build (consolidates v14+v15)
    RAPM_VOL6_NO1_Portada_v7.tex    — canonical portada source
    RAPM_VOL6_NO1_Contraportada_v3.tex  — canonical contraportada
    Informe_Cierre_Editorial_V6N1.tex   — closure report
    README.md                       — build instructions + QA checklist

┌──────────────────────────────────────────────────────────────────────┐
│ SECTION 8 · OVERALL HEALTH SCORE                                      │
└──────────────────────────────────────────────────────────────────────┘

  Functional output:           ✓ 10/10  (volume ships correctly)
  Code reproducibility:        ⚠  6/10  (requires v14+v15 sequence)
  Code cleanliness:            ⚠  5/10  (magic numbers, no error handling)
  Documentation:               ✗  2/10  (no README, no inline docs)
  Disk hygiene:                ✗  3/10  (~46 MB reclaimable)
  Test coverage:               ✗  1/10  (only one-off QA scripts)

  OVERALL:  FUNCTIONAL BUT UNTIDY
  Priority: (1) delete legacy artifacts, (2) consolidate to single pipeline,
  (3) add README.md with build recipe.
