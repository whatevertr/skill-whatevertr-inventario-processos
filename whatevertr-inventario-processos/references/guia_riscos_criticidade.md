# Guia de Riscos e Criticidade (apoio à inferência)

Referência de apoio para **inferir e classificar riscos** — usada tanto pela skill de inventário (que infere os riscos) quanto pela de diagnóstico (que os prioriza). **Não é verdade fixa:** é âncora para a IA raciocinar. Tudo o que a IA gerar aqui é **inferência (laranja)** e precisa de validação humana.

---

## 1. Como a criticidade é calculada

Fórmula clássica:

> **Criticidade (ou Risco) = Probabilidade × Impacto**

- **Impacto** — o tamanho do estrago se o risco se materializa (financeiro, legal, operacional, reputacional).
- **Probabilidade** — quão provável/frequente é acontecer.

A skill **infere a probabilidade** (não a tira de lugar nenhum) — por isso ela entra como inferência (laranja) e é apoio, nunca dado auditado.

### A IA pode (e deve) conversar para calibrar — não é um bot de esteira
O gatilho da skill é um **pedido** (documentar, mapear, achar gaps, analisar riscos de processo). A partir daí a instância **dialoga com quem pediu** — não precisa processar em silêncio e cuspir a tabela. Para calibrar a probabilidade, pode perguntar direta ou indiretamente algo que revele a **frequência**:
- Direto: "esse erro acontece com que frequência? toda semana, todo mês?"
- Indireto: "quantas notas passam por aqui por dia?", "já aconteceu esse mês?", "isso trava sempre ou foi pontual?"

A resposta do usuário sobre frequência **deixa de ser inferência** e vira dado (troca de laranja para grafite). Se o usuário não souber, mantém-se a probabilidade inferida (laranja), marcada como tal.

## 2. Matriz de risco (para plotar a criticidade)

Ferramenta visual para posicionar cada risco por Probabilidade × Impacto. Use **3x3** (simples) ou **5x5** (mais fina):

```
Impacto ↑
 Alto   | Médio | Alto  | Crítico
 Médio  | Baixo | Médio | Alto
 Baixo  | Baixo | Baixo | Médio
        +----------------------→ Probabilidade
          Baixa   Média   Alta
```

A faixa (Baixo/Médio/Alto/Crítico) vira a **ordem de criticidade** que a skill de diagnóstico usa para montar o plano de ação.

## 3. Tabela-guia: tipo de risco × criticidade típica

Apoio para a IA **inferir a que tipo um risco pertence** e qual criticidade típica ele carrega. A criticidade real varia com o negócio — esta coluna é ponto de partida, não veredito.

| Tipo de Risco | Criticidade típica | Impacto principal | Exemplo (neutro) |
|---|---|---|---|
| **Fraudes e Segurança da Informação** | Muito Alta | Vazamento de dados, desvio financeiro, perda de rastreabilidade física/sistêmica | Mercadoria faturada parada na expedição sem registro nem transporte, exposta a desvio sem rastro; usuário sem bloqueio dá baixa em estoque sem revisão nem controle de acesso |
| **Conformidade (Legal)** | Alta | Multas, processos, passivo tributário, paralisação | Descumprimento de LGPD ou norma ambiental; cobrança/faturamento indevido a cliente que já cancelou; saldo gerado com mercadoria ainda em trânsito |
| **Falhas em Sistemas e Tecnologia** | Média a Alta | Interrupção da operação, ausência de rotina sistêmica, dados irreais | Queda do ERP; inexistência de rotina para cancelar documento em trânsito; amostra com classificação semântica errada gerando relatório falso |
| **Riscos Físicos e Ambientais** | Média | Dano ao patrimônio, risco à integridade da equipe | Curto-circuito em maquinário; alagamento do estoque |
| **Erros de Planejamento e Processos** | Alta | Custo logístico desnecessário, perda de controle de estoque, retrabalho massivo | Falta de sincronia entre chegada física e faturamento (status "em trânsito" para item ainda no armazém); ausência de critério unificado de aceite; SLA estourando por amarração sistêmica |
| **Falhas Humanas** | Baixa a Média | Refugo, retrabalho, pequenos atrasos; em cadeia sem controle, perda definitiva | Erro de digitação em nota/relatório; despacho de item já cancelado por falta de conferência; ausência de romaneio para validar entrega de terceiro |

**Como usar:** para cada processo, ao varrer as 5 categorias de risco (ver `inferencia.md` §2), use esta tabela para (a) nomear o tipo, (b) estimar a criticidade típica, (c) ajustar pela probabilidade inferida/perguntada. O resultado alimenta a ordem de criticidade do diagnóstico.

## 4. Todo risco puxa uma oportunidade que o mitiga

Regra que amarra risco e melhoria (detalhe em `inferencia.md`): **o nº de oportunidades é ≥ o nº de riscos**, porque cada risco recebe uma oportunidade de mitigação com **ID simétrico** (R01↔O01, R02↔O02…). As oportunidades **extras** (que não mitigam risco específico, mas melhoram o processo) vêm depois, a partir de O(n+1). Assim a criticidade de cada risco já nasce ligada à ação que o trata — sem precisar de uma coluna de controle separada.

---
*Guia de apoio — NUD (Constellation Method), Thainá Ramos. Conteúdo inferido pela IA a partir deste guia é sempre inferência (laranja) sujeita a validação humana.*
