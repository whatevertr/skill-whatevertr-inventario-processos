---
name: whatevertr-inventario-processos
description: "Use SEMPRE que o usuário pedir para preencher, criar, atualizar ou consolidar um Inventário de Processos no modelo SIPOC-R personalizado (Modelo_Inventario_Processos.xlsx). Acione também quando enviar insumos brutos — áudio, transcrição, .pptx, .docx, políticas, procedimentos, anotações, fluxograma em PDF — pedindo para 'mapear processos', 'documentar', 'transformar em SIPOC', 'levantar', 'organizar em planilha de processos', 'consolidar no inventário', ou expressões equivalentes. Acione ainda quando descrever oralmente/em texto demandas e tarefas pedindo para organizá-las como processo. Analisa insumos com técnica de processos, separa múltiplos processos em linhas distintas, infere riscos/oportunidades (análise por categoria inspirada em FMEA, só severidade) e legislação aplicável (LGPD, CLT), marcando as inferências pela COR do texto (laranja = inferido) e por ID sequencial contínuo (E01, R01, O01), e entrega .xlsx no padrão exato do modelo (Excel Table, cores, estrutura)."
license: CC-BY-4.0
---

# Inventário de Processos — Skill de Preenchimento

Esta skill converte **insumos brutos** (áudio, transcrição, PPT, DOCX, PDF, anotações, descrições orais) em **linhas estruturadas** do Inventário de Processos no modelo SIPOC-R personalizado, aplicando técnica de análise de processos.

## Princípios inegociáveis

1. **Fidelidade ao modelo.** A estrutura do `Modelo_Inventario_Processos.xlsx` (16 colunas, Excel Table, freeze, cores, linha de instrução em L4, linha de exemplo em L5) é **inviolável**. Nunca alterar colunas, ordem, nomes ou layout. (A coluna "Controle / Mitigação" foi removida na v3 — a mitigação virou a oportunidade simétrica; ver Fase 4.)

2. **Uma linha = uma unidade de processo no nível de granularidade escolhido (N1/N2/N3).** O que conta como "uma linha" depende do nível — ver «Nível de granularidade do inventário» abaixo. Critérios de separação em `references/tecnica_processos.md`.

3. **Não inventar fatos.** Campos como Responsável, SLA, Sistemas, Indicador, Fornecedor, Cliente: **só preencher quando o insumo trouxer** a informação ou for explicitamente inferível com alta confiança. Se ausente, deixar vazio (não usar "N/A", "-", "a definir").

4. **Inferência permitida só em três campos** — Legislação, Riscos e Oportunidades. A origem de cada item é marcada pela **COR do texto**, e Riscos/Oportunidades recebem **ID sequencial**:
   - **Legislação**: inferir apenas o óbvio (LGPD se há dado pessoal, CLT se há gestão de pessoas, normas técnicas se há produção/SST). Conservador.
   - **Riscos**: varredura por categoria **inspirada em FMEA, só severidade** (operacional, conformidade, prazo, qualidade, financeiro) — não calcula RPN.
   - **Oportunidades**: melhorias típicas (automação, padronização, integração, eliminação de retrabalho).

   **Convenção de cor e ID** (detalhe em `references/inferencia.md`):
   - **Laranja** = inferido pela skill · **violeta negrito** = literal do insumo e importante · **grafite** = literal normal. A cor diz a ORIGEM; o negrito diz a IMPORTÂNCIA.
   - **IDs contínuos no inventário inteiro:** etapas `E01, E02…`, riscos `R01, R02…`, oportunidades `O01, O02…` — **nunca reiniciam por célula**.
   - **Repetição:** risco/oportunidade que reaparece em outra etapa **reusa o mesmo ID**, marcado com **🍷** (repetição inferida, a validar).

5. **Premissas do modelo são lei.** As premissas escritas na aba `Premissas` do modelo (granularidade, verbos no infinitivo, não usar "N/A", convenção de cor, etc.) devem ser respeitadas integralmente — e devem estar sincronizadas com este SKILL.md. **SIPOC-R = SIPOC + Riscos** (o "R" é a extensão de Riscos do NUD; não confundir com o "R" de *Requirements* usado por outras fontes).

6. **Output sempre é arquivo .xlsx.** Nunca entregar uma tabela em markdown como produto final — apenas como preview se o usuário pedir confirmação antes do arquivo.

## Nível de granularidade do inventário (N1 · N2 · N3)

A unidade de uma linha **não é fixa** — depende do objetivo do inventário. A mesma realidade pode ser registrada em três níveis. Em todos eles, a unidade do responsável é a **função/responsabilidade** (posto de trabalho: setor, célula ou gestão), **nunca a pessoa como indivíduo**.

| Nível | Unidade da linha | Critério de corte | Objetivo típico |
|---|---|---|---|
| **N1 — Macro** | 1 processo inteiro | Gatilho / cliente / saída diferentes | Inventariar, contar, priorizar no alto nível |
| **N2 — Posto de trabalho** *(padrão)* | 1 **segmento** de um posto (bloco contíguo entre dois handoffs) | **Cada handoff** (troca do posto responsável) | Ver o que cada posto faz em cada passagem; **alimenta o fluxograma BPMN** |
| **N3 — Intra-posto** *(raro)* | 1 função (carregada por 1 pessoa) ou 1 automação | Troca de função dentro do posto; sistema autônomo vira linha própria | Detalhar uma área única quando o escopo inteiro vive nela |

**Critério de corte de N2 (o coração).** Corta-se por **segmento entre handoffs**. Um segmento é o bloco **contíguo** de trabalho de um posto, do bastão que ele **recebe** até o bastão que ele **passa**. Regras:

- **Tarefas coladas do mesmo posto, sem ninguém no meio** → **uma linha** (ex.: o confeiteiro separa os ingredientes e, em seguida, mistura a massa = uma linha).
- **Mesmo posto que sai e volta**, com **outros postos no meio** → **duas linhas** (dois segmentos). Ex.: o confeiteiro prepara a massa (passa o bastão para o forno), o forno assa, e **volta** ao confeiteiro para desenformar e decorar = **dois segmentos = duas linhas**.
- Não se corta por troca de tarefa, de sistema nem de momento **dentro** de um segmento — só nos handoffs (entrada e saída do bastão).
- **Automação autônoma é um posto** (responsável "Automação") e **gera handoff**: robô que executa sozinho → segmento próprio; sistema só operado por alguém fica em *Sistemas/Recursos*, não vira linha.
- **Ramo de exceção** (nota que trava, desvio, retrabalho) corta por handoff **como qualquer outro** — cada passagem de bastão no desvio é um segmento. Nunca uma linha genérica que esconde 2-3 postos. Vira sub-processo à parte só se tiver gatilho/entrada/saída próprios.
- **Cerca de escopo (obrigatória):** antes de cortar, declarar em *Comentários* (e na nota de entrega) os **fluxos incluídos e excluídos** deste levantamento. Fluxo citado de passagem, adiado ou de outro produto **fica FORA** — não se puxa para dentro. Detalhes e exemplos em `references/tecnica_processos.md` §3B.

*Exemplo completo (Fazer um bolo, N2):* (1) confeiteiro prepara a massa → (2) forno assa → (3) confeiteiro desenforma e decora. O confeiteiro é **um posto** (uma raia no fluxo) em **dois segmentos** (linhas 1 e 3 na tabela).

**Teste do corolário.** Uma linha = um responsável. O **mesmo posto pode aparecer em mais de uma linha** (segmentos diferentes) — o que não pode é uma linha ter mais de um responsável. Se a coluna *Responsável* precisa de mais de um posto, a linha é N1 de propósito ou está macro demais e deve quebrar em N2.

**N3 — intra-posto (raro e sensível).** Só quando o processo inteiro vive dentro de uma área única. A unidade desce para a **função/responsabilidade** dentro do posto — não para a pessoa como indivíduo; a pessoa é só quem normalmente carrega aquela função. Um **sistema só vira linha própria quando executa a tarefa de forma autônoma** (sem ação humana); nesse caso o responsável é **"Automação"**. Sistema apenas operado por alguém **não** é linha — fica no campo *Sistemas/Recursos* da função que o opera. (Espelha o roxo "atividade automatizada" da skill de fluxograma.)

**N3 pede mais perguntas.** É o nível mais sensível: sempre que a divisão estiver duvidosa, **perguntar antes de cortar** — não inferir calado. Difuso em N3 = (a) não dá pra nomear uma função única para um trecho, ou (b) função e pessoa não são 1:1 (uma pessoa com várias funções, ou várias pessoas numa mesma função).

### Escolha do nível — perguntar sempre, sugerindo o mais provável

O nível é decisão de objetivo, então **a skill sempre pergunta qual N usar** (com `ask_user_input_v0` se disponível, em formato de menu). A pergunta **já vem com a sugestão** do nível que mais encaixa, marcada como recomendada. Inferir a sugestão assim:

- Insumo descreve **várias áreas trocando o bastão** e/ou o objetivo é desenhar fluxo → sugerir **N2**.
- Insumo é um **levantamento amplo de muitos processos** para registro/priorização → sugerir **N1**.
- Insumo é o **detalhamento de uma área só** → sugerir **N3**.

O menu apresenta as três opções com uma linha de explicação cada e o nível sugerido marcado como "(recomendado)". Se o usuário **não responder** e o trabalho precisar seguir, usar o nível sugerido e **registrar a escolha em Comentários**.

### Contrato de consistência com a skill de fluxograma

O fluxograma BPMN **pressupõe N2**, com a correspondência: **raia = posto** (um posto = uma raia, mesmo que reentre) e **linha da tabela = segmento**. Um posto que sai e volta tem **1 raia e 2+ linhas**; no desenho, o **conector A** marca a fronteira entre os segmentos (onde uma linha vira a outra). Inventário que vai virar fluxo precisa estar em N2; se estiver em N1, **explodir para N2 antes** de gerar o fluxo. Misturar níveis entre as duas skills produz fluxos que não casam com a tabela.

> **Fundamento (para não virar adereço):** N1 ≈ níveis de inventário do APQC PCF; N2 ≈ raia de Rummler-Brache / BPMN (corte no *handoff* / *white space*; a raia identifica o *performer*, que é papel/função, não pessoa); N3 ≈ sub-raia aninhada de BPMN. O corte se dá nos **handoffs** (entrada/saída do bastão), não por pessoa/lugar/tempo dentro do segmento — escolha deliberada e alinhada a BPMN.

## Fluxo de trabalho

A skill executa em **5 fases**. Cada fase tem checkpoint claro antes de avançar.

### Fase 1 — Identificar insumos e modo de operação

Antes de ler insumos, decidir o **modo**:

- **Modo INCREMENTO**: usuário anexou um `Modelo_Inventario_Processos.xlsx` (ou variante) **já com linhas preenchidas além da linha 5 de exemplo**. A skill lê a numeração existente, continua a partir do próximo número, e preserva o que já está lá.
- **Modo NOVO**: usuário não anexou inventário existente, OU anexou apenas o modelo limpo. A skill gera arquivo do zero usando `scripts/builder.py`.

Verificação técnica:

```python
from openpyxl import load_workbook
wb = load_workbook(caminho)
ws = wb['Inventário de Processos']
# Linha 5 é o exemplo. Linhas 6+ com algo na coluna B (Nome do Processo) = inventário em uso.
em_uso = any(ws.cell(row=r, column=2).value for r in range(6, ws.max_row + 1))
```

Se `em_uso=True` → modo INCREMENTO. Senão → modo NOVO.

**Nível de granularidade.** Além do modo, decidir o **nível (N1/N2/N3)** — sempre perguntando ao usuário (menu) com a sugestão do nível que mais encaixa no insumo. Ver «Nível de granularidade do inventário».

### Fase 2 — Ler e extrair conteúdo dos insumos

Cada formato tem um caminho de leitura. Detalhes em `references/leitura_insumos.md`.

Resumo:

| Insumo | Ferramenta |
|---|---|
| Áudio (.mp3, .wav, .m4a, .ogg) | Pedir transcrição prévia ao usuário — esta skill **não transcreve áudio**, mas processa transcrições |
| Transcrição (.txt, colado em chat) | Texto direto |
| PPT (.pptx) | `extract-text arquivo.pptx` |
| Word (.docx) | `extract-text arquivo.docx` |
| PDF de texto | `pdftotext` ou pypdf — ver `references/leitura_insumos.md` |
| PDF de fluxograma (imagens) | Rasterizar e analisar visualmente — ver `references/leitura_insumos.md` |
| Anotações, descrição oral em chat | Texto direto |

**Importante:** ao ler, **preservar contexto temporal e atribuição**. Quem fala? Sobre qual processo? Qual o trecho que sustenta cada inferência? Isso será usado em Comentários quando houver ambiguidade.

### Fase 3 — Analisar com técnica de processos

Esta é a fase mais crítica. Detalhes em `references/tecnica_processos.md`. Resumo do método:

1. **Listar candidatos a processo** — qualquer trecho que descreva uma atividade recorrente com início, transformação e entrega.

2. **Aplicar critérios de separação de linhas:**
   - **Gatilho diferente** → linha diferente (ex.: "Reporte mensal" vs "Reporte sob demanda")
   - **Cliente final diferente** → linha diferente (ex.: "Relatório para diretoria" vs "Relatório para equipe")
   - **Saída diferente** → linha diferente
   - **Mesmo gatilho + cliente + saída** → consolidar em uma linha
   - **Tarefa não recorrente** (algo que acontece uma vez) → NÃO entra no inventário; sinalizar ao usuário
   - **Corte dependente do nível:** os critérios acima são o corte de **N1**. Em **N2**, corta-se por **segmento entre handoffs** (cada troca do posto responsável; um posto que reentra com outros no meio = mais de uma linha). Em **N3**, por **função / automação** (nunca por pessoa-indivíduo). Ver «Nível de granularidade do inventário».

3. **Mapear cada processo identificado para os 16 campos**, usando as heurísticas de extração em `references/mapeamento_campos.md` (S/I/P/O/C, Gatilho, SLA, etc.).

4. **Identificar lacunas** — campos onde o insumo não trouxe informação. Decidir entre: deixar vazio, inferir (texto em laranja, com ID), ou perguntar ao usuário (apenas para ambiguidades centrais — granularidade, separação de linhas).

### Fase 4 — Inferir Legislação, Riscos e Oportunidades

Aplicar as regras de inferência. Detalhes em `references/inferencia.md`.

**Legislação (conservador — texto inferido em laranja):**
- Dados pessoais (CPF, e-mail, contato, foto, salário, avaliação) → LGPD
- Gestão de pessoas (admissão, demissão, ponto, férias, PPR) → CLT (e LGPD se houver dado pessoal)
- Produção, manuseio, SST → Normas Regulamentadoras aplicáveis (a validar qual NR)
- Financeiro/fiscal → Legislação fiscal/contábil aplicável
- Sem indicador claro → **deixar vazio**

**Riscos (inspirado em FMEA, só severidade):**
Para cada processo, varrer 5 categorias e listar 1-3 riscos plausíveis. Cada risco recebe **ID contínuo** (`R01`, `R02`… sem reiniciar) e texto em laranja:
1. **Operacional** — erro humano, falha de sistema, retrabalho
2. **Prazo** — atraso, fila, dependência externa
3. **Conformidade** — descumprimento de norma, ausência de evidência
4. **Qualidade** — informação incorreta, divergência entre bases
5. **Financeiro/Reputacional** — perda financeira, impacto em cliente

Para classificar a **criticidade** de cada risco (Probabilidade × Impacto), apoie-se em `references/guia_riscos_criticidade.md`. A probabilidade é **inferida** (laranja); a instância **pode conversar com o usuário** para calibrar a frequência — não é bot de esteira.

**Oportunidades (ID contínuo `O01`, `O02`… em laranja) — ordem obrigatória:**
- **Primeiro, a mitigação de cada risco, com ID simétrico** (R01↔O01, R02↔O02…). Todo risco tem uma oportunidade que o mitiga → **nº de oportunidades ≥ nº de riscos**.
- **Depois, as extras** (O n+1…): automação (Power Query/VBA/Python/RPA), integração/dashboard, template/checklist, centralização/repositório único.
- Risco repetido (🍷) → mitigação repetida (mesmo O, 🍷). Detalhe em `references/inferencia.md` §3.0.

**Marcação:** a origem é a **cor** (laranja = inferido · violeta negrito = literal importante · grafite = literal). Riscos e oportunidades levam **ID contínuo** no inventário inteiro; repetição do mesmo risco/oportunidade **reusa o ID** com 🍷. No campo Comentários: `Itens em laranja são inferência da skill; 🍷 = repetição de ID inferida — validar.`

### Fase 5 — Gerar/atualizar o arquivo

Usar `scripts/builder.py` (ver `references/builder.md` para a API).

**Modo NOVO:**
```bash
python scripts/builder.py --output /mnt/user-data/outputs/Inventario_Processos.xlsx --linhas <json_com_linhas>
```

**Modo INCREMENTO:**
```bash
python scripts/builder.py --base <arquivo_anexado> --output /mnt/user-data/outputs/Inventario_Processos_atualizado.xlsx --linhas <json_com_linhas>
```

Após gerar, apresentar com `present_files` e fazer **resumo enxuto**:

```
Inventário gerado com N processos. Pontos de atenção:
- Linhas X, Y: granularidade pode estar ampla — revisar
- Itens em LARANJA são inferência da skill (Legislação: Z linhas, Riscos: R01..RNN, Oportunidades: O01..ONN); 🍷 = repetição de ID inferida — validar
- Campos vazios principais: Indicador (N), SLA (N), Responsável (N) — sem info no insumo
```

## Anti-padrões — o que NÃO fazer

- ❌ **Não consolidar processos com gatilhos diferentes na mesma linha** ("Reporte mensal e Reporte sob demanda" → 2 linhas, não 1)
- ❌ **Não inventar SLA, Responsável, Sistemas ou Indicador.** Se não está no insumo, deixar vazio.
- ❌ **Não preencher legislação como "Política interna"** sem que o insumo mencione política específica. Política interna não é legislação no sentido estrito; vai em Comentários se relevante.
- ❌ **Não escrever riscos em forma de problema atual** ("O processo é lento"). Risco é potencial ("R01 Atraso na entrega por dependência de áreas externas").
- ❌ **Não confundir oportunidade com solução técnica detalhada.** Oportunidade é a direção da melhoria ("O01 Automação da coleta de indicadores"), não a especificação ("Criar VBA com 3 macros").
- ❌ **Não excluir a linha de exemplo (L5)** ao incrementar — preservar; novas linhas começam em L6 ou na próxima vazia.
- ❌ **Não mexer em colunas, ordem, cores ou layout** do modelo.
- ❌ **Não entregar markdown como produto final** — sempre gerar o .xlsx.

## Quando pedir confirmação ao usuário

Pergunte (com `ask_user_input_v0` se disponível) apenas nestes casos:

1. **Nível de granularidade** — sempre perguntar (menu N1/N2/N3 com o nível sugerido marcado como recomendado). Ver «Nível de granularidade do inventário».
2. **Separação de linhas duvidosa** — você não tem certeza se dois trechos são o mesmo processo ou processos distintos. Mostrar a separação proposta e pedir OK.
3. **Modo INCREMENTO + conflito de código** — você detectou que o processo novo pode já existir no inventário. Perguntar se incrementa ou substitui.
4. **Divisão difusa em N3** — perguntar antes de cortar (não inferir): quando (a) não dá pra nomear uma função única para um trecho, ou (b) função e pessoa não são 1:1.

Para o resto (legislação, riscos, oportunidades): **proceda com a inferência em laranja (ID contínuo) e deixe o usuário validar depois**, não trave o fluxo.

## Resumo da entrega

Toda execução termina com:
1. Arquivo .xlsx em `/mnt/user-data/outputs/` apresentado via `present_files`
2. Resumo curto em texto: quantos processos, quais lacunas, quais inferências (em laranja) foram aplicadas
3. Recomendação de próximos passos (revisar o que está em laranja e com 🍷, validar SLAs com responsáveis, etc.)

**Recado obrigatório ao usuário, com destaque:** ⚠️ Tudo em LARANJA é inferência da IA e tudo com 🍷 é repetição de ID inferida — as duas camadas precisam de conferência humana antes do uso. O violeta negrito marca o que veio do insumo e foi apontado como importante.

## Documentos de referência

Carregue conforme necessário durante a execução:

- **`references/tecnica_processos.md`** — critérios de identificação e separação de processos (leia na Fase 3)
- **`references/mapeamento_campos.md`** — como cada campo do SIPOC é extraído do texto bruto (leia na Fase 3)
- **`references/leitura_insumos.md`** — como ler cada formato de insumo (leia na Fase 2)
- **`references/inferencia.md`** — regras detalhadas e exemplos para Legislação, Riscos e Oportunidades (leia na Fase 4)
- **`references/guia_riscos_criticidade.md`** — tipo de risco × criticidade, matriz Probabilidade × Impacto, mitigação simétrica (leia na Fase 4)
- **`references/builder.md`** — API do script de geração do .xlsx (leia na Fase 5)
- **`assets/Modelo_Inventario_Processos.xlsx`** — modelo de referência (estrutura base que o builder reproduz)
