<p align="right"><a href="README.md">🇺🇸 English</a></p>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-night.png">
  <img alt="whatevertr-inventario-processos — insumos brutos viram um Inventário de Processos SIPOC-R em .xlsx" src="assets/banner-day.png">
</picture>

# whatevertr-inventário-processos

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

Esta é uma **skill que eu fiz para o Claude** (Anthropic) para transformar insumos brutos — transcrição, áudio, `.pptx`, `.docx`, políticas, procedimentos, anotações e fluxograma em PDF — em um **Inventário de Processos** no modelo **SIPOC-R**, entregue em `.xlsx` pronto para uso. Fiz para o meu próprio trabalho de engenharia de processos e uso todo dia; deixo aqui caso seja útil pra você também.

Faz parte do **NUD | Constellation Method**, de Thainá Ramos.

> **Como eu uso & compatibilidade:** empacotei como **Claude Skill** (formato Agent Skills da Anthropic, então aciona sozinha no Claude Code / claude.ai). É **projetada para ser agnóstica de modelo** — o método é só `SKILL.md` + `references/`, então também colo como contexto em outros LLMs de chat, e o `builder.py` é Python puro (já rodei no Code Interpreter do ChatGPT). Tudo que precisa pra instalar e rodar está neste repositório, e eu sigo melhorando isso pra ficar fácil de pegar.
>
> **Sobre evidência, com honestidade:** o que eu garanto é o meu uso — funciona pra mim. Você consegue reproduzir a saída a partir do repositório. O quanto o *método* generaliza além dos meus casos é algo que eu ainda estou aprendendo, e eu ia adorar teu retorno se você testar.

---

## O que ela faz

- Lê o insumo com técnica de processos e **separa cada processo em uma linha** (um responsável por linha).
- Preenche o padrão **SIPOC-R**: Fornecedor · Entrada · Processo · Responsável · Saída · Cliente, mais SLA, Indicador, Sistemas, Legislação, Riscos, Oportunidades.
- **Infere riscos (inspirado em FMEA, só severidade) e legislação aplicável** e marca cada inferência pela COR do texto (laranja) e por ID contínuo (R01, O01) — as inferências ficam sinalizadas explicitamente para você validar, pra suposição não passar por fato.
- Escolhe o **nível de granularidade** (N1 macro · N2 por handoff · N3 intra-posto) perguntando a você, com a sugestão mais provável.
- Entrega um **Excel no formato do modelo** (tabela, cores, estrutura).

> **SIPOC-R = SIPOC + Riscos** — a extensão de Riscos do NUD. Não é o "R" de *Requirements*.

Para a análise consolidada de riscos (matriz priorizada, visão de riscos e oportunidades), use a skill complementar **[whatevertr-diagnóstico-de-riscos](https://github.com/whatevertr/skill-whatevertr-diagnostico-de-riscos)**.

## Estrutura

```
whatevertr-inventario-processos/
├── SKILL.md                         # instruções da skill
├── assets/
│   └── Modelo_Inventario_Processos.xlsx   # modelo de saída (exemplo: "Fazer um bolo")
├── references/                      # técnica de processos, mapeamento de campos, inferência, builder
└── scripts/
    └── builder.py                   # gera o .xlsx a partir das linhas
```

## Como instalar

Copie a pasta `whatevertr-inventario-processos/` para o diretório de skills do seu Claude
(`.claude/skills/`) e a skill passa a ser acionada pelos gatilhos descritos no `SKILL.md`.

## Exemplo

O modelo traz um processo neutro de exemplo — **"Fazer um bolo de cenoura"** — para você ver o
preenchimento antes de rodar com os seus próprios processos. Substitua ou exclua a linha de
exemplo antes do uso real.

## Licença

[CC-BY-4.0](LICENSE). Uso livre, com atribuição.

---

*NUD (Constellation Method) — método de Thainá Ramos (Nud by Whatevertr) · <https://github.com/whatevertr> · Licenciado sob CC-BY-4.0.*
