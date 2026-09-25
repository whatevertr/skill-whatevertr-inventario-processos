<p align="right"><a href="README.md">🇺🇸 English</a></p>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-night.png">
  <img alt="nud-inventario-processos — insumos brutos viram um Inventário de Processos SIPOC-R em .xlsx" src="assets/banner-day.png">
</picture>

# nud-inventário-processos

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

Uma **skill para Claude** (Anthropic) que transforma insumos brutos: transcrição, áudio, `.pptx`, `.docx`, políticas, procedimentos, anotações e fluxograma em PDF em um **Inventário de Processos** no modelo **SIPOC-R**, entregue em `.xlsx` pronto para uso.

Faz parte do **NUD | Constellation Method**, de Thainá Ramos.

> **Compatibilidade:** empacotada como **Claude Skill** (formato Agent Skills da Anthropic, aciona sozinha no Claude Code / claude.ai). O **método é agnóstico de modelo**: o mesmo conteúdo funciona em **qualquer LLM de chat** colando o `SKILL.md` + `references/` como contexto, e o `builder.py` roda em **qualquer Python** (ex.: Code Interpreter do ChatGPT).

---

## O que ela faz

- Lê o insumo com técnica de processos e **separa cada processo em uma linha** (um responsável por linha).
- Preenche o padrão **SIPOC-R**: Fornecedor · Entrada · Processo · Responsável · Saída · Cliente, mais SLA, Indicador, Sistemas, Legislação, Riscos, Oportunidades.
- **Infere riscos (inspirado em FMEA, só severidade) e legislação aplicável** e marca cada inferência pela COR do texto (laranja) e por ID contínuo (R01, O01) para o usuário validar — nunca apresenta suposição como fato.
- Escolhe o **nível de granularidade** (N1 macro · N2 por handoff · N3 intra-posto) perguntando ao usuário, com a sugestão mais provável.
- Entrega um **Excel no padrão exato do modelo** (tabela, cores, estrutura).

> **SIPOC-R = SIPOC + Riscos** — a extensão de Riscos do NUD. Não é o "R" de *Requirements*.

Para a análise consolidada de riscos (matriz priorizada, causa-raiz, visão executiva), use a skill complementar **[nud-diagnóstico-de-riscos](https://github.com/whatevertr/skill-nud-diagnostico-de-riscos)**.

## Estrutura

```
nud-inventario-processos/
├── SKILL.md                         # instruções da skill
├── assets/
│   └── Modelo_Inventario_Processos.xlsx   # modelo de saída (exemplo: "Fazer um bolo")
├── references/                      # técnica de processos, mapeamento de campos, inferência, builder
└── scripts/
    └── builder.py                   # gera o .xlsx a partir das linhas
```

## Como instalar

Copie a pasta `nud-inventario-processos/` para o diretório de skills do seu Claude
(`.claude/skills/`) e a skill passa a ser acionada pelos gatilhos descritos no `SKILL.md`.

## Exemplo

O modelo traz um processo neutro de exemplo — **"Fazer um bolo de cenoura"** — para você ver o
preenchimento antes de rodar com os seus próprios processos. Substitua ou exclua a linha de
exemplo antes do uso real.

## Licença

[CC-BY-4.0](LICENSE). Uso livre, com atribuição.

---

*NUD (Constellation Method) — método de Thainá Ramos (Nud by Whatevertr) · <https://github.com/whatevertr> · Licenciado sob CC-BY-4.0.*
