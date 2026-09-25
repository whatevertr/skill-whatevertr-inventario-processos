# Mapeamento de Campos — Como Extrair Cada Coluna do Texto Bruto

Para cada uma das 16 colunas do inventário, este documento traz: o que extrair, como reconhecer no texto, exemplos e regras de "deixar vazio".

## 1. Código/N°

**Conteúdo:** número sequencial (1, 2, 3...). O modelo já vem com numeração pré-populada na coluna A.

**Como preencher:**
- **Modo NOVO**: usar a numeração que já está no modelo (linhas 6+ já têm 1, 2, 3...).
- **Modo INCREMENTO**: ler o último número usado e continuar a sequência.

**Nunca:** deixar vazio. Nunca pular números.

---

## 2. Nome do Processo

**Conteúdo:** nome curto e claro, começando com **verbo no infinitivo + objeto**.

**Bons exemplos:**
- "Reportar Diretoria Mensalmente"
- "Consolidar Indicadores de Performance"
- "Ajustar Painéis no sistema de RH"
- "Aprovar Solicitações de Férias"

**Maus exemplos (corrigir):**
- "Reporte de diretoria" → substantivo, falta verbo → "Reportar Diretoria"
- "Gestão do sistema de RH" → genérico demais → quebrar em processos específicos
- "Clicar em exportar no sistema de RH" → granular demais (é tarefa)

**Nunca:** deixar vazio. Se o insumo não nomeou, **crie um nome** a partir das ações descritas.

---

## 3. Gatilho

**Conteúdo:** o que dispara o processo. Categorias:

| Tipo | Exemplo |
|---|---|
| **Calendário** | "Toda 1ª segunda do mês", "Diariamente às 8h", "Trimestral" |
| **Demanda** | "Quando a gerência solicita", "Sob demanda da diretoria" |
| **Evento** | "Quando entra um chamado", "Após fechamento contábil" |
| **Sistema** | "Quando o sistema de RH dispara alerta", "Ao receber e-mail no inbox X" |

**Como extrair do texto:**
- Procurar advérbios de tempo ("toda", "sempre que", "diariamente", "ao final de", "quando")
- Procurar verbos de gatilho ("é solicitado", "é disparado", "chega", "entra")

**Se ambíguo:** preencher com a melhor inferência + nota em Comentários.

**Deixar vazio:** raríssimo — todo processo tem gatilho. Se o insumo não traz, perguntar ao usuário.

---

## 4. Fornecedor (S)

**Conteúdo:** quem fornece a entrada. Pessoa, área, sistema ou cliente externo.

**Como extrair:**
- "Pego os dados **do sistema de RH**" → Fornecedor: sistema de RH
- "**RH** me passa a planilha" → Fornecedor: RH
- "Recebo do **gestor**" → Fornecedor: Gestor (papel)

**Múltiplos fornecedores:** separar por vírgula. Ex.: "sistema de RH, RH, Áreas de backoffice"

**Deixar vazio:** se o insumo não trouxer informação sobre origem da entrada.

---

## 5. Entrada (I)

**Conteúdo:** o que efetivamente entra no processo — informação, base de dados, documento, recurso.

**Como extrair:**
- "Pego os **indicadores consolidados**" → Entrada: Indicadores consolidados
- "Preciso da **planilha de admissões do mês**" → Entrada: Planilha de admissões mensais
- "**Chamados** do sistema de chamados" → Entrada: Chamados (sistema de chamados)

**Distinção crítica:** Fornecedor é **quem**, Entrada é **o quê**. Não confundir.

**Múltiplas entradas:** separar com quebra de linha (Alt+Enter no Excel — usar `\n` no Python).

**Deixar vazio:** se o insumo não detalha o que entra.

---

## 6. Processo (P)

**Conteúdo:** macropassos do processo — 3 a 7 passos curtos, numerados, descrevendo a transformação.

**Estrutura recomendada:**
```
1. [Verbo] [objeto] [contexto opcional]
2. [Verbo] [objeto]
3. ...
```

**Bom exemplo:**
```
1. Coletar indicadores do sistema de RH e bases auxiliares
2. Consolidar no template padrão de reporte
3. Validar números com gerência da área
4. Enviar PPT final à diretoria por e-mail
```

**Maus exemplos:**
- Texto corrido sem passos → reorganizar em itens numerados
- 15 passos detalhados → consolidar em macropassos (3-7)
- 1 passo só ("Gerar relatório") → faltou desdobrar

**Como extrair do texto:**
- Buscar sequências temporais: "primeiro... depois... aí... no final"
- Verbos de ação que aparecem em sequência
- Se a fala é desorganizada, **reordenar logicamente** os passos

**Deixar vazio:** muito raro. Se o insumo só dá nome do processo sem descrever passos, perguntar ao usuário.

---

## 7. Responsável

**Conteúdo:** quem executa. **Preferir papel a nome de pessoa** (rotatividade).

**Como extrair:**
- "**Eu** faço" → Responsável: [papel do usuário, ex. Analista de Gestão]
- "O **time de backoffice** executa" → Responsável: Time de Backoffice
- "É o **analista de processos**" → Responsável: Analista de Processos

**Se o insumo citou nome:** usar `Nome (Papel)` — ex.: "João Silva (Analista de Gestão)".

**Deixar vazio:** se o insumo não identifica executor.

---

## 8. Saída (O)

**Conteúdo:** o entregável concreto do processo.

**Como extrair:**
- "No final eu **mando um PPT**" → Saída: PPT executivo
- "**Atualizo a base**" → Saída: Base cadastrada atualizada
- "**Aprovo o pedido**" → Saída: Pedido aprovado (decisão registrada)

**Distinção crítica:** saída ≠ atividade. "Consolidar dados" é atividade; saída é "Base consolidada".

**Deixar vazio:** raríssimo. Todo processo tem entregável; sem ele, não é processo.

---

## 9. Cliente (C)

**Conteúdo:** quem consome a saída.

**Como extrair:**
- "Mando **pra diretoria**" → Cliente: Diretoria
- "**Equipe usa** o painel" → Cliente: Equipe
- "É consumido **pelo cliente externo**" → Cliente: Cliente externo (ou nome específico se citado)

**Múltiplos clientes:** se a saída é a mesma para todos, separar por vírgula. Se a saída muda por cliente, **separar em linhas diferentes** (ver `tecnica_processos.md` §3.2).

**Deixar vazio:** raro. Se não há cliente, provavelmente não é processo.

---

## 10. SLA

**Conteúdo:** prazo ou periodicidade acordada.

**Formatos comuns:**
- "Mensal — entrega até D+5 útil"
- "1x/mês toda 1ª segunda"
- "Até 4h após o gatilho"
- "Imediato (≤30min)"

**Como extrair:**
- Procurar números + unidade de tempo
- Procurar "deadline", "até", "no máximo"
- Distinguir **periodicidade** (com que frequência roda) de **prazo de execução** (quanto tempo até entregar após o gatilho)

**Não inferir:** se o insumo não cita SLA, **deixar vazio**. Não chutar baseado em "parece razoável".

---

## 11. Indicador

**Conteúdo:** Nome do KPI + meta. Enxuto — um indicador-chave.

**Formatos:**
- "Aderência ao prazo ≥ 95%"
- "TMR ≤ 2h"
- "Taxa de retrabalho ≤ 5%"

**Como extrair:**
- Procurar menções a "métrica", "indicador", "KPI", "meta", percentuais
- Se o insumo cita um número-meta sem nome, inventar um nome curto

**Não inferir:** se o insumo não cita indicador, **deixar vazio**. (Diferente de Riscos/Oportunidades — em Indicador não inferimos.)

---

## 12. Sistemas / Recursos

**Conteúdo:** sistemas, softwares e ferramentas usados.

**Como extrair:**
- Nomes próprios de software/sistema citados literalmente
- "Pacote Office", "ERP", "sistema de RH", "Power BI", "sistema de chamados", "Excel", "VBA"

**Não inferir:** se o insumo não cita ferramenta, **deixar vazio**.

---

## 13. Legislação Aplicável

Ver `inferencia.md` §1. Inferência conservadora em LARANJA, ou literal (grafite) se citada.

---

## 14. Riscos

Ver `inferencia.md` §2. Inferência ampla em LARANJA, com ID contínuo `R01, R02…` (inspirada em FMEA, só severidade).

---

## 15. Oportunidades

Ver `inferencia.md` §3. Inferência ampla em LARANJA, com ID contínuo `O01, O02…`. **Ordem obrigatória:** primeiro a oportunidade que mitiga cada risco, com ID simétrico (R01↔O01); depois as extras. Nº de oportunidades ≥ nº de riscos. (A antiga coluna "Controle / Mitigação" foi removida — a mitigação agora é a oportunidade simétrica.)

---

## 16. Comentários

**Conteúdo:** informações relevantes que não cabem nas outras colunas + **registro de decisões da skill**.

**Sempre incluir aqui (quando aplicável):**
- "Inferências em Legislação/Riscos/Oportunidades são sugestões a validar."
- "Processo separado de [Linha N] por diferença de gatilho/cliente/saída."
- "Granularidade escolhida em conjunto com usuário."

**Outros conteúdos:**
- Dependências entre processos
- Histórico relevante ("Automação despriorizada para 2026")
- Restrições conhecidas
