# Leitura de Insumos

Como extrair conteúdo de cada tipo de insumo. Aplicar na Fase 2 da skill.

## Áudio (.mp3, .wav, .m4a, .ogg)

**Esta skill não transcreve áudio diretamente.**

Se o usuário enviar áudio:

1. Verificar se já foi transcrito (texto colado, .txt anexo, ou transcrição embutida no chat)
2. Se não houver transcrição, pedir ao usuário que envie a transcrição (Claude.ai/Cowork podem ter ferramentas de transcrição em outras etapas, mas esta skill consome texto)

Mensagem ao usuário:
> "Recebi o áudio mas esta skill processa texto. Posso seguir se você me enviar a transcrição (mesmo crua, com erros). Ou, se preferir, descreva os pontos principais — eu organizo a partir daí."

## Transcrição de fala (texto)

Características:
- Fala associativa — pessoas pulam entre processos
- Sem pontuação clara, parágrafos longos
- Marcadores de hesitação ("né", "tipo", "aí") — ignorar
- Misturam contexto pessoal com descrição de processo

**Estratégia:**
1. Ler a transcrição inteira primeiro, sem extrair nada
2. Listar candidatos a processo (qualquer atividade recorrente mencionada)
3. Reler buscando o gatilho/cliente/saída de cada candidato
4. Aplicar critérios de separação de linhas (`tecnica_processos.md` §3)

## PowerPoint (.pptx)

Ferramenta:
```bash
extract-text /mnt/user-data/uploads/arquivo.pptx
```

Saída: texto por slide, com "## Slide N" como cabeçalho. Notas do apresentador (speaker notes) também são extraídas quando presentes.

**Padrões comuns em decks de processo:**

- **Slide de macroprocesso** (diagrama de caixas): cada caixa principal **costuma** virar 1 processo (ou várias linhas se a caixa contiver subprocessos). Como o extract-text traz só o texto, perguntar ao usuário se há diagrama relevante que se perdeu na extração.
- **Slide de "Responsabilidades" / "Atividades"**: cada bullet costuma ser 1 processo, mas validar com critérios de granularidade.
- **Speaker notes**: frequentemente contêm o gatilho, SLA e responsável que não aparecem nos bullets do slide.

Se a extração ficar pobre (muitas imagens, pouco texto), considerar abrir slides como imagens e analisar visualmente — ver `/mnt/skills/public/pptx/SKILL.md`.

## Word (.docx)

Ferramenta:
```bash
extract-text /mnt/user-data/uploads/arquivo.docx
```

Saída: markdown com headings, listas, tabelas preservados.

**Padrões comuns:**

- **POP/Procedimento formal**: 1 documento ≈ 1 processo. O próprio documento costuma trazer Objetivo, Escopo, Responsáveis, Atividades — mapear cada para a coluna correspondente.
- **Política institucional**: macroprocesso. Não tentar extrair múltiplas linhas sem pedir foco ao usuário.
- **Manual operacional**: vários processos. Listar as seções e tratar cada uma como candidato.

Se houver tabelas no DOCX, elas vêm como tabelas markdown — ótimo, dados estruturados.

## PDF — texto extraível

Verificação rápida:
```bash
pdftotext -f 1 -l 1 /mnt/user-data/uploads/arquivo.pdf - | head
```

Se sair texto legível, prosseguir:
```bash
pdftotext /mnt/user-data/uploads/arquivo.pdf /tmp/texto.txt
```

Tratar como Word: ler, identificar candidatos, mapear campos.

## PDF — fluxograma ou imagens

Quando `pdftotext` retorna pouco ou nada, o PDF é provavelmente baseado em imagens (scan, fluxograma vetorial mal extraído, etc.).

Caminhos possíveis (ler `/mnt/skills/public/pdf-reading/SKILL.md`):

1. **Rasterizar páginas como imagem** e analisar visualmente — Claude consegue interpretar fluxogramas de imagem:
   ```python
   # Ver pdf-reading skill para detalhes
   import subprocess
   subprocess.run(['pdftoppm', '-png', '-r', '150',
                   '/mnt/user-data/uploads/arq.pdf', '/tmp/pag'])
   ```
   Depois, com a imagem em vista, identificar as caixas/raias do fluxo.

2. **OCR** se for scan de texto.

**Padrão de fluxograma:**
- **Caixa inicial** = gatilho do processo
- **Caixas intermediárias** = passos do "Processo (P)"
- **Caixa final** = saída + cliente
- **Raias (swimlanes)** = responsáveis diferentes (atenção: pode indicar separação em processos diferentes ou apenas múltiplos atores em um mesmo processo — usar critérios de `tecnica_processos.md`)
- **Losangos** = decisões — refletir como passos com bifurcação no texto do Processo (P)

## Anotações / texto colado no chat

Mais fácil: já é texto. Aplicar mesma lógica de transcrição.

Atenção a:
- Listas com bullets ou hífens — frequentemente já estão pré-separadas em processos/tarefas
- Tabelas em markdown — podem mapear quase direto

## Múltiplos insumos numa mesma execução

Quando o usuário envia vários arquivos:

1. Ler todos antes de começar a mapear
2. Identificar se descrevem **os mesmos processos** (informações complementares) ou **processos diferentes**
3. Se complementares: consolidar antes de mapear
4. Se distintos: mapear cada conjunto separadamente, na ordem que faz sentido

## Sinais de qualidade dos insumos

Antes de mapear, avaliar:

- **Insumo rico**: descreve gatilho + atividades + saída + cliente → mapear com confiança
- **Insumo médio**: descreve atividades mas falta cliente ou gatilho → mapear o que dá, deixar lacunas vazias
- **Insumo pobre**: só nomes de tarefas soltas → pedir mais contexto antes de gerar arquivo (não inventar)

Se insumo for muito pobre, **avisar o usuário** em vez de gerar um inventário fraco:
> "Os insumos que recebi descrevem [X processos] mas não trazem informação suficiente sobre gatilho/cliente/SLA. Posso gerar o inventário com lacunas (campos vazios) ou você prefere complementar antes?"
