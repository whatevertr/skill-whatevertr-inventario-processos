# Técnica de Análise de Processos

Este documento descreve como identificar processos em um texto bruto e separá-los corretamente em linhas do inventário. É o coração da skill.

## 1. O que é um processo (para fins deste inventário)

**Definição operacional:** uma atividade ou conjunto de atividades **recorrentes**, com:
- **Gatilho identificável** (algo dispara — calendário, demanda, evento de sistema)
- **Entrada** (insumo: informação, base, recurso)
- **Transformação** (passos executados por uma pessoa/sistema)
- **Saída** (entregável concreto)
- **Cliente** (alguém consome a saída)

Se faltar qualquer um desses 5 elementos, **não é processo ainda** — é tarefa solta, evento único ou projeto. Vai virar pergunta ao usuário ou nota no resumo, não linha no inventário.

## 2. Granularidade — escolhendo o nível certo

Os três níveis mais comuns:

| Nível | Exemplo | Vai no inventário? |
|---|---|---|
| **Macroprocesso** | "Gestão de Performance" | ❌ Amplo demais — quebrar em processos |
| **Processo** | "Reportar Diretoria Mensal" | ✅ Sim — esse é o nível alvo |
| **Tarefa/atividade** | "Abrir o sistema de RH e exportar relatório X" | ❌ Granular demais — vira passo dentro de "Processo (P)" |

**Sinais de macroprocesso (precisa quebrar):**
- Nome genérico ("Gestão de X", "Suporte a Y")
- Mais de 1 gatilho diferente
- Mais de 1 cliente final diferente
- Saída descrita como categoria, não como entregável ("relatórios diversos", "análises")

**Sinais de tarefa (precisa agregar a um processo maior):**
- Verbo muito específico de UI ("Clicar em X", "Abrir aba Y")
- Não tem cliente claro
- Faz parte de uma sequência maior já mapeada

## 3. Critérios para SEPARAR em linhas diferentes

Use estes critérios em ordem. Se **qualquer um** for "sim", separe em duas linhas.

### 3.1. Gatilhos diferentes → linhas diferentes

Exemplo:
> "Faço o reporte de diretoria toda primeira segunda do mês, e também faço relatórios ad-hoc quando a gerência pede."

→ **2 linhas:**
- Linha A: Reporte Mensal de Diretoria (gatilho: calendário)
- Linha B: Relatório Ad-hoc para Gerência (gatilho: demanda)

Por quê: SLA, periodicidade, prioridade e riscos mudam completamente.

### 3.2. Clientes diferentes → linhas diferentes

Exemplo:
> "Consolido os indicadores e mando o reporte para a diretoria e também uma versão simplificada pra equipe."

→ **2 linhas:**
- Linha A: Reporte Executivo (cliente: Diretoria, saída: PPT executivo)
- Linha B: Comunicação de Resultados à Equipe (cliente: Equipe, saída: e-mail/Slack resumido)

Por quê: o que é entregue muda, o nível de detalhe muda, a frequência pode mudar.

### 3.3. Saídas estruturalmente diferentes → linhas diferentes

Exemplo:
> "Faço o ajuste dos painéis no sistema de RH e também ajusto a base cadastrada quando vejo desvio."

→ **2 linhas:**
- Linha A: Ajuste de Painéis sistema de RH (saída: painel atualizado)
- Linha B: Correção de Base Cadastrada sistema de RH (saída: base corrigida)

Por quê: são entregáveis distintos com fluxos distintos.

### 3.4. Mesma fórmula em contextos diferentes → linhas diferentes

Exemplo:
> "Faço a análise de meta detratora para o time de operações e a mesma análise para o time comercial."

→ **2 linhas** se os times exigem cortes/critérios diferentes; **1 linha com escopo "múltiplas áreas"** se a metodologia é idêntica. Pergunte ao usuário se houver dúvida.

## 3B. Corte em N2 — por HANDOFF (e os casos que confundem)

Os critérios de §3 (gatilho/cliente/saída) são o corte de **N1**. Em **N2** — o nível padrão, que alimenta o fluxograma — o corte é **por handoff**. Esta seção resolve os quatro casos que mais geram divergência entre execuções.

### 3B.1. O que é um handoff (definição operacional)

**Handoff = passagem do bastão entre postos** — o momento em que **quem executa muda**. Um posto entrega o trabalho e outro posto assume.

- **Um segmento** = o bloco **contíguo** de trabalho de **um mesmo posto**, do bastão que ele recebe até o bastão que ele passa. **Um segmento = uma linha.**
- **Teste único:** *"o responsável mudou?"* Se sim, houve handoff → nova linha. Se não (o mesmo posto segue trabalhando, mudando só de tarefa, de sistema ou de sala), **continua a mesma linha**.
- **Não confundir com N1:** em N2 **não** se corta por gatilho/cliente/saída, e **não** se funde dois postos numa "macro-etapa" só porque o tema é o mesmo. Handoff manda. (Fundir captura + cadastro em uma linha quando são postos diferentes é o erro clássico — são dois segmentos.)

### 3B.2. Automação é um posto

Um **sistema/robô que executa a etapa de forma autônoma** (sem ação humana no meio) **é um posto** — o responsável é **"Automação"** — e portanto **gera handoff**. Ex.: robô captura e classifica a nota (posto Automação) → pessoa cadastra o SKU (posto humano) = **dois segmentos**, porque o bastão passou do robô para a pessoa.

Sistema que é **apenas operado** por alguém (a pessoa clica, o sistema responde) **não** é posto próprio — fica no campo *Sistemas / Recursos* da linha daquele operador.

### 3B.3. Ramo de exceção (a nota que trava, o desvio, o retrabalho)

Quando o fluxo **desvia** — a nota trava e vai para outro posto tratar, depois volta — esse desvio **não é uma linha genérica** que engole tudo. Regra:

- **Cada passagem de bastão dentro do desvio é um segmento como qualquer outro.** Se a nota travada vai para o Fiscal e volta para a Automação, são (no mínimo) dois handoffs → linhas próprias.
- Só vira **sub-processo à parte** (fora deste inventário, com sua própria linha-mãe) quando tem **gatilho + entrada + saída próprios e recorrência independente**. Se é contínuo ao fluxo principal, corta normal, por handoff.
- **Nunca** resolver a exceção com uma única linha vaga do tipo "Tratar nota travada" que esconde 2-3 postos diferentes. Explicite os segmentos.

### 3B.4. Cerca de escopo (in/out) — declarar ANTES de cortar

Antes de segmentar, **declarar explicitamente** o que está dentro e o que está fora deste levantamento — e **registrar em Comentários** (ou na nota de entrega). Um fluxo que aparece **só de passagem**, foi **adiado para outra reunião**, ou é de **outro produto/processo**, fica **FORA** e é anotado como excluído — **não se puxa para dentro** do inventário.

Exemplo: numa reunião sobre entrada de nota de **peça**, alguém cita de passagem a compra de **pneu**. Pneu **não entra** (escopo excluído: "fluxo de pneu — mencionado, não mapeado nesta reunião"). Puxar o pneu para dentro é espalhamento — o anti-padrão que a cerca previne.

## 4. Critérios para CONSOLIDAR em uma linha

Junte em uma linha só quando **todos** abaixo forem verdadeiros:

- Mesmo gatilho
- Mesmo cliente final
- Mesma natureza de saída
- Mesmo responsável

Diferenças menores (ferramenta auxiliar, formato do arquivo) **não** justificam linhas separadas.

Exemplo de consolidação:
> "Pra fazer o reporte eu pego dados do sistema de RH, do Excel e do Power BI."

→ **1 linha:** Reporte de Diretoria — Sistemas: sistema de RH, Excel, Power BI

## 5. Heurísticas para extrair processos de cada tipo de insumo

### Áudio/transcrição de fala livre

Pessoas descrevem demandas de forma associativa, pulando entre processos. **Não confie na ordem da fala** — releia e agrupe por gatilho/cliente.

Marcadores linguísticos úteis:
- "**Toda** segunda…", "**Sempre que**…", "**Mensalmente**…" → indicam recorrência (= processo)
- "**Uma vez** fiz…", "**Esse ano** vou fazer…" → indica evento único (NÃO é processo)
- "**Eu também faço** X" → provavelmente novo processo, criar linha
- "**Inclusive eu pego** Y" → pode ser entrada do mesmo processo, não novo processo

### Apresentações (.pptx)

Decks de processo costumam ter:
- Slide com diagrama de macroprocesso → identificar quais caixas viram linhas
- Slides de "responsabilidades da área" → cada item costuma ser 1 processo
- Slides de "atividades" → ler com cuidado, pode ser tarefa, não processo

### Documentos Word / políticas / procedimentos

- Procedimentos formais (POP, IT) costumam mapear 1 documento = 1 processo
- Políticas mais amplas (ex.: "Política de Comunicação") são macroprocesso — pedir foco ao usuário antes de tentar quebrar

### Fluxogramas (PDF)

- Cada raia (swimlane) costuma indicar uma responsabilidade — não necessariamente um processo
- Início e fim do fluxo geralmente delimitam **um** processo
- Múltiplos fluxos no mesmo PDF → múltiplos processos

## 6. Quando pedir confirmação ao usuário

Pergunte (não chute) quando:

1. **Granularidade está ambígua** — exemplo: "Gestão do sistema de RH" pode virar 1 processo amplo ou 4 processos médios. Mostre as duas opções.
2. **Você identificou algo que pode ser projeto, não processo** — exemplo: "Desenvolvimento de ferramenta de automação" pode ser um projeto único (não vai no inventário) ou um processo recorrente de desenvolvimento.
3. **Você está em dúvida sobre separar ou consolidar duas atividades** — mostre a proposta e peça OK.

Não pergunte sobre:
- Inferências de legislação/risco/oportunidade — sempre em LARANJA, com ID contínuo (R0x/O0x)
- Lacunas em SLA, Responsável, Indicador — deixe vazio e sinalize no resumo

## 7. Checklist mental antes de gerar o arquivo

- [ ] Cada linha tem nome de processo começando com verbo no infinitivo
- [ ] Cada linha tem gatilho identificável
- [ ] Nenhuma linha consolida dois clientes/gatilhos diferentes
- [ ] Nenhuma linha é uma tarefa solta (sem cliente claro)
- [ ] Nenhuma linha é um projeto único (sem recorrência)
- [ ] Inferências marcadas pela COR (laranja) e por ID contínuo em Legislação, Riscos, Oportunidades
- [ ] Comentários explicam decisões não óbvias (granularidade, consolidação, inferências)
