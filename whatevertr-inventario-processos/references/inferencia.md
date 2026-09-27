# Inferência — Legislação, Riscos e Oportunidades

Apenas três campos do inventário admitem inferência da skill: **Legislação, Riscos e Oportunidades**.

Duas coisas marcam o conteúdo desses campos:
1. **ID sequencial** para Riscos (`R01`, `R02`…) e Oportunidades (`O01`, `O02`…) — ver «Sistema de IDs».
2. **Cor do texto**, que diz a **origem** de cada item — ver «Convenção de cor».

> A cor substitui a antiga marcação `[a][b][c]`. Agora a origem (inferido × literal) é lida pela cor, e a numeração é contínua no inventário inteiro.

---

## Sistema de IDs

- **Etapas / processos:** cada linha do inventário tem um ID na coluna Código/N°: `E01`, `E02`, `E03`… (contínuo). O prefixo pode ser do contexto quando fizer sentido (ex.: `DEV-01` para devolução), mas o padrão neutro da skill é `E01`.
- **Riscos:** `R01`, `R02`, `R03`… **contínuo no inventário inteiro, nunca reinicia por célula.**
- **Oportunidades:** `O01`, `O02`, `O03`… mesma regra.

Exemplo de numeração contínua entre linhas:

```
E01 | R01, R02 | O01, O02
E02 | R03, R04 | O03, O04
```

### Risco ou oportunidade que se repete → reusa o MESMO ID

Se o mesmo risco aparece em mais de uma etapa (mesma causa/efeito), ele **mantém o ID** em todas, mesmo que a redação mude um pouco. Exemplo: um risco de "falta de conferência" que existe na etapa E01 e na E03 é `R02` nas duas.

- A skill **infere** quando dois riscos são o mesmo. Como é inferência, **marca com 🍷** (taça) para o humano validar.
- Se a skill errar (juntar dois que eram diferentes, ou separar dois iguais), o humano corrige na revisão — por isso a taça.

---

## Convenção de cor (diz a ORIGEM; o negrito diz a IMPORTÂNCIA)

| Origem do item | Importância | Cor do texto | Negrito |
|---|---|---|---|
| **Inferido** pela skill | normal | laranja | não |
| **Inferido** pela skill | importante | laranja | **sim** |
| **Literal** do insumo (o usuário citou) | importante | violeta | **sim** |
| **Literal** do insumo | normal | grafite (padrão) | não |

Regra em uma linha: **laranja = a IA inferiu · violeta = veio do insumo · negrito = é importante.** A cor nunca mente sobre a origem; o negrito só chama atenção.

Hex sugeridos (a autora pode ajustar para a paleta NUD): laranja `#993700`, violeta `#642DA4`, grafite `#191128`.

### Exemplo de célula Riscos com mistura

Insumo do usuário: "Esse processo tem o risco do extrato bancário vir desatualizado, e isso é o mais grave."

```
R01  Extrato bancário desatualizado          ← literal + importante → VIOLETA NEGRITO
R02  Operacional: divergência entre bases     ← inferido normal → laranja
R03  Conformidade: lançamento sem nota fiscal ← inferido normal → laranja
```

O primeiro item veio do insumo e o usuário disse que é o mais grave → violeta negrito. Os demais são inferência da skill → laranja.

---

## 1. Legislação Aplicável (inferência conservadora)

**Regra geral:** apontar a(s) **legislação(ões) que regem ou auditam a etapa** — aquelas cujo **descumprimento gera consequência para a companhia** (multa, autuação, processo, passivo). Não é listar toda lei que "tem a ver com o tema"; é a norma que, se não respeitada naquela etapa, cobra um preço. Quando não houver uma norma com essa força, **deixar vazio** (não inferir por inferir). Legislação inferida vai em **laranja**; legislação citada literalmente pelo usuário vai em **grafite** (ou violeta negrito se o usuário destacar como crítica).

### 1.1. Gatilhos para inferência

| Sinal no insumo / processo | Inferência (em laranja) |
|---|---|
| Dado pessoal (CPF, e-mail, telefone, foto, salário, avaliação individual, endereço, saúde) | LGPD |
| Gestão de pessoas (admissão, demissão, ponto, férias, folha, PPR, treinamento) | CLT + LGPD (se houver dado pessoal) |
| Produção, manufatura, manuseio físico, operação em campo | Normas Regulamentadoras aplicáveis (a validar qual NR) |
| Processo financeiro/fiscal (nota fiscal, lançamento contábil, conciliação) | Legislação fiscal/contábil aplicável |
| Saúde, prontuário, paciente | LGPD + CFM/Anvisa (a validar) |
| Contratos, compliance, licitação | Legislação contratual aplicável (a validar) |
| SAC, atendimento ao consumidor | CDC + LGPD |

### 1.2. Casos que parecem "óbvios" mas NÃO são

- "Política interna da empresa" → não é legislação. Vai em Comentários se relevante.
- "Padrão ISO 9001" → norma técnica voluntária, não legislação. Comentários ou vazio.
- Processos administrativos sem dado pessoal nem regulamento → **deixar vazio**, não inferir.

---

## 2. Riscos (inspirado em FMEA, só severidade)

> **Nota de método:** esta varredura é **inspirada no FMEA**, mas usa **só o eixo de severidade/impacto** — não calcula RPN nem usa os eixos de ocorrência e detecção do FMEA clássico. É uma análise qualitativa de riscos por categoria, não um FMEA completo.

**Regra geral:** para cada processo, varrer 5 categorias e listar **1 a 3 riscos plausíveis**, cada um com seu ID (`R0x`) em laranja. Riscos literais do insumo entram em grafite (ou violeta negrito se o usuário destacar como críticos).

### 2.1. Categorias e perguntas-guia

**Operacional** — atividade manual repetitiva (erro humano); dependência de sistema único (indisponibilidade); retrabalho (inconsistência).
**Prazo** — SLA apertado (atraso); dependência de áreas externas (espera); volumetria variável (pico não absorvido).
**Conformidade** — legislação aplicável (descumprimento); requisito de evidência (ausência de registro); aprovação obrigatória (fluxo bypassado).
**Qualidade** — múltiplas fontes consolidadas à mão (divergência); validação humana subjetiva (critério inconsistente); transcrição/digitação (erro de transcrição).
**Financeiro / Reputacional** — afeta pagamento/cobrança/faturamento (risco financeiro direto); comunicação externa (reputacional); decisão sobre cliente/colaborador (impacto pessoal).

### 2.2. Estrutura da inferência

Cada risco em uma linha: `R0x  [Categoria curta]: [descrição do potencial]`.

Exemplo, para o processo "Fazer um bolo por encomenda":
```
R01  Qualidade: fermento vencido faz a massa não crescer
R02  Prazo: forno ocupado atrasa a entrega no dia combinado
R03  Conformidade: falha de higiene na manipulação
```

### 2.3. O que NÃO é risco

- **Problema atual e recorrente** ("Sempre atrasa") → é problema, não risco. Vira **Oportunidade**.
- **Descrição genérica** ("Risco operacional") → sem conteúdo, precisa ser específico.
- **Solução** ("Falta de automação") → é oportunidade, não risco.

### 2.4. Volume

Limite-se a **3 riscos por processo**, os mais plausíveis. Mais que isso vira ruído.

### 2.5. Criticidade (apoio, sempre inferida)

Para classificar a gravidade de cada risco, use o **`references/guia_riscos_criticidade.md`** (tipo de risco × criticidade típica × impacto, matriz Probabilidade × Impacto). Pontos-chave:
- **Criticidade = Probabilidade × Impacto.** A skill **infere** a probabilidade (laranja) — é apoio, não dado auditado.
- **A instância pode conversar com o usuário** para calibrar a frequência (pergunta direta "acontece toda semana?" ou indireta "quantas notas passam por dia?"). Resposta do usuário sobre frequência vira dado (grafite), não inferência. A skill **não é um bot de esteira** — dialoga.

### 2.6. Cada risco puxa uma oportunidade que o mitiga

Todo risco listado terá, em Oportunidades, uma melhoria que o **mitiga**, com **ID simétrico** (R01↔O01). Isso substitui a antiga coluna "Controle / Mitigação" — a mitigação agora vive na oportunidade. Ver §3.

---

## 3. Oportunidades (inferência ampla)

**Regra geral:** cada uma com ID (`O0x`) em laranja. Oportunidades literais do insumo entram em grafite.

### 3.0. Ordem obrigatória: mitigação primeiro, extras depois

O nº de oportunidades é **≥** o nº de riscos, porque **todo risco tem uma oportunidade que o mitiga**. Monte nesta ordem:

1. **Para cada risco, liste a oportunidade que o mitiga, com ID simétrico:** R01→O01, R02→O02, … Rn→On. (Pode indicar "(mitiga R0x)" no texto.)
2. **Só depois** liste as oportunidades **extras** (melhoria do processo que não trata um risco específico): O(n+1), O(n+2)…
3. **Risco repetido** (mesmo ID, 🍷) → **mitigação repetida** (mesmo O, 🍷).

Exemplo: riscos R01–R03 num processo → oportunidades O01 (mitiga R01), O02 (mitiga R02), O03 (mitiga R03), depois O04, O05 extras. Assim a criticidade de cada risco já nasce ligada à ação — sem coluna de controle separada.

### 3.1. Padrões de oportunidade (em laranja)

| Sinal no processo | Oportunidade típica |
|---|---|
| Atividade manual repetitiva | Automação (Power Query/VBA/Python/RPA) |
| Múltiplas fontes consolidadas à mão | Integração em base única / dashboard |
| Conferência/validação manual | Controle automatizado / validação por regra |
| Falta de padrão visível | Padronização via template / checklist |
| Tempo gasto buscando informação | Centralização em repositório único |
| Transcrição entre sistemas | Integração via API / exportação direta |
| Aprovação por e-mail | Workflow de aprovação em ferramenta dedicada |

### 3.2. Quando NÃO sugerir

- Processo simples e bem desenhado — não forçar.
- Insumo já cita a oportunidade — usar literal (grafite).
- Oportunidade que seria refazer todo o processo — isso é projeto, não oportunidade pontual.

### 3.3. Granularidade

Oportunidade é **direção**, não especificação técnica. ✅ `O01 Automação da coleta de indicadores` · ❌ detalhar macros/ODBC (isso vira projeto).

### 3.4. Volume

**Mínimo:** uma oportunidade de mitigação por risco (§3.0) — logo, nº de oportunidades **≥** nº de riscos. **Extras:** até ~2 por processo, as mais plausíveis; mais que isso vira ruído.

---

## 4. Como sinalizar inferências no arquivo final

Em toda linha com inferência (Legislação, Riscos ou Oportunidades):
1. **Cor** cada item conforme a origem (laranja = inferido, grafite/violeta = literal) — ver «Convenção de cor».
2. **ID** contínuo (`R0x`, `O0x`), reusando o ID em repetições (com 🍷).
3. **Comentários** (coluna 16): registrar `Itens em laranja são inferência da skill; itens com 🍷 são repetição de ID inferida — validar.`

### Exemplo de linha completa

| Campo | Conteúdo | Cor |
|---|---|---|
| Legislação | LGPD | laranja (inferida) |
| Riscos | R01 Operacional: erro manual na consolidação · R02 Prazo: atraso por dependência de áreas | laranja |
| Oportunidades | O01 Automação da coleta · O02 Centralização das bases | laranja |
| Comentários | Itens em laranja são inferência da skill — validar. |

---

## 5. Como o usuário consome essas inferências (recado obrigatório na entrega)

Ao entregar o arquivo, a skill **deve** avisar o usuário, com destaque:

> ⚠️ **Tudo em LARANJA é inferência da IA. Tudo com 🍷 é repetição de ID inferida. As duas camadas precisam de conferência humana antes do uso.** O violeta negrito marca o que veio do insumo e foi apontado como importante; confira também.

O analista que recebe o arquivo deve: filtrar o que está em laranja e o que tem 🍷, confirmar/ajustar/remover item por item pelo ID, e trocar a cor para grafite quando o item for validado.
