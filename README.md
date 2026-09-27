<p align="right"><a href="README.pt-BR.md">🇧🇷 Português</a></p>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-night.png">
  <img alt="nud-inventario-processos — raw inputs into a SIPOC-R Process Inventory in .xlsx" src="assets/banner-day.png">
</picture>

# nud-inventario-processos

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

This is a **skill I built for Claude** (Anthropic) to turn raw inputs — transcripts, audio, `.pptx`, `.docx`, policies, procedures, notes and PDF flowcharts — into a **Process Inventory** in the **SIPOC-R** model, delivered as a ready-to-use `.xlsx`. I made it for my own process-engineering work and use it daily; I'm sharing it here in case it's useful to you too.

Part of the **NUD | Constellation Method**, by Thainá Ramos.

> **How I use it & compatibility:** I package it as a **Claude Skill** (Anthropic's Agent Skills format, so it triggers on its own in Claude Code / claude.ai). It's **designed to be model-agnostic** — the method is just `SKILL.md` + `references/`, so I also paste it as context into other chat LLMs, and `builder.py` is plain Python (I've run it in ChatGPT's Code Interpreter). Everything needed to install and run is in this repo, and I keep improving that so it's easy to pick up.
>
> **On evidence, honestly:** what I can vouch for is my own use — it works for me. You can reproduce the output yourself from the repo. How well the *method* generalizes beyond my cases is something I'm still learning, and I'd love to hear from you if you test it.

---

## What it does

- Reads the input with process technique and **puts each process on its own row** (one owner per row).
- Fills the **SIPOC-R** model: Supplier · Input · Process · Owner · Output · Customer, plus SLA, Indicator, Systems, Legislation, Risks, Opportunities.
- **Infers risks (FMEA-inspired, severity only) and applicable legislation**, marking every inference by text COLOR (orange) and a continuous ID (R01, O01) — the inferences are flagged explicitly for you to validate, so a guess doesn't pass as fact.
- Chooses the **granularity level** (N1 macro · N2 per handoff · N3 intra-station) by asking you, with the most likely suggestion.
- Delivers an **Excel in the model's format** (table, colors, structure).

> **SIPOC-R = SIPOC + Risks** — the NUD Risk extension. It is not the "R" for *Requirements*.

For the consolidated risk analysis (prioritized matrix, risk-and-opportunity view), use the companion skill **[nud-diagnostico-de-riscos](https://github.com/whatevertr/skill-nud-diagnostico-de-riscos)**.

## Structure

```
nud-inventario-processos/
├── SKILL.md                         # skill instructions
├── assets/
│   └── Modelo_Inventario_Processos.xlsx   # output model (example: "Bake a cake")
├── references/                      # process technique, field mapping, inference, builder
└── scripts/
    └── builder.py                   # generates the .xlsx from the rows
```

## Install

Copy the `nud-inventario-processos/` folder into your Claude skills directory (`.claude/skills/`) and the skill starts triggering on the cues described in `SKILL.md`.

## Example

The model ships a neutral example process — **"Bake a carrot cake"** — so you can see the fill-in before running it with your own processes. Replace or delete the example row before real use.

## License

[CC-BY-4.0](LICENSE). Free to use, with attribution.

---

*NUD (Constellation Method) — a method by Thainá Ramos (Nud by Whatevertr) · <https://github.com/whatevertr> · Licensed under CC-BY-4.0.*
