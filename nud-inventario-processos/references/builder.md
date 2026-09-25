# Builder — API e uso

Script: `scripts/builder.py`

## Função

Inserir/atualizar linhas no Inventário de Processos preservando **100%** da estrutura visual do modelo (Excel Table, cores, freeze panes, linha 4 de instrução, linha 5 de exemplo, larguras, bordas).

O builder **nunca** mexe em:
- Linhas 1-5 do arquivo (nota, legendas, headers, instrução, exemplo)
- Aba Premissas
- Estrutura de colunas (ordem, nomes, cores de header)
- Excel Table (apenas atualiza o `ref` para abranger as novas linhas)

## Uso

### Modo NOVO (parte do modelo limpo do asset)

```bash
python scripts/builder.py \
  --output /mnt/user-data/outputs/Inventario_Processos.xlsx \
  --linhas linhas.json
```

### Modo INCREMENTO (parte de arquivo já preenchido)

```bash
python scripts/builder.py \
  --base /mnt/user-data/uploads/Inventario_atual.xlsx \
  --output /mnt/user-data/outputs/Inventario_atualizado.xlsx \
  --linhas linhas.json
```

### Inline (JSON direto na linha de comando)

Útil para 1-2 linhas:

```bash
python scripts/builder.py \
  --output /mnt/user-data/outputs/saida.xlsx \
  --linhas '[{"Nome do Processo": "Reportar Diretoria", "Gatilho": "Mensal"}]'
```

## Formato do JSON de linhas

Lista de objetos. Uma chave por coluna do inventário. **Código/N° é automático** — não incluir no JSON.

```json
[
  {
    "Nome do Processo": "Reportar Diretoria Mensalmente",
    "Gatilho": "Calendário — toda 1ª segunda do mês",
    "Fornecedor (S)": "Áreas de backoffice, sistema de RH, RH",
    "Entrada (I)": "Indicadores consolidados, atas, PPT padrão",
    "Processo (P)": "1. Coletar indicadores\n2. Consolidar\n3. Validar\n4. Enviar",
    "Responsável": "Analista de Gestão",
    "Saída (O)": "Apresentação executiva (.pptx)",
    "Cliente (C)": "Cliente que encomendou",
    "SLA": "Mensal — D+5 útil",
    "Indicador": "Aderência ao prazo ≥ 100%",
    "Sistemas / Recursos": "sistema de RH, Pacote Office, Power BI",
    "Legislação Aplicável": [{"texto": "Boas práticas (RDC Anvisa)", "origem": "inferido"}],
    "Riscos": [{"id": "R01", "texto": "Qualidade: fermento vencido nao cresce", "origem": "inferido"}, {"id": "R02", "texto": "Prazo: forno ocupado atrasa a entrega", "origem": "inferido"}],
    "Oportunidades": [{"id": "O01", "texto": "Conferir validade do fermento (mitiga R01)", "origem": "inferido"}, {"id": "O02", "texto": "Reservar forno com antecedencia (mitiga R02)", "origem": "inferido"}, {"id": "O03", "texto": "Padronizar em ficha tecnica", "origem": "inferido"}],
    "Comentários": "Itens em laranja sao inferencia da skill; repeticao de ID inferida (taca) — validar."
  }
]
```

## Nomes exatos das colunas

Devem bater **exatamente** com o cabeçalho do modelo (linha 3). Diferenças de acentuação, espaço ou caractere especial vão fazer o campo ficar vazio:

```
Código/N°
Nome do Processo
Gatilho
Fornecedor (S)
Entrada (I)
Processo (P)
Responsável
Saída (O)
Cliente (C)
SLA
Indicador
Sistemas / Recursos
Legislação Aplicável
Riscos
Oportunidades
Comentários
```

## Quebras de linha dentro de uma célula

Usar `\n` no JSON (Python interpreta como newline; Excel renderiza com wrap_text).

## Campos vazios

Se uma chave estiver ausente do dict, OU tiver valor `null`, OU string vazia `""`, a célula fica vazia. **Não** escrever "N/A", "-" ou "nenhum".

## Comportamento do código (Coluna A)

- O builder lê o maior número já presente na coluna A (apenas em linhas que tenham `Nome do Processo` preenchido na coluna B).
- A próxima linha recebe `ultimo + 1`.
- Modo NOVO sobre o asset: começa em 1 (o asset tem números pré-populados, mas como nenhuma linha tem nome, são ignorados).
- Modo INCREMENTO: continua da numeração existente.

## Verificação pós-geração

Após rodar o builder, **sempre** validar:

```python
from openpyxl import load_workbook
wb = load_workbook('saida.xlsx')
ws = wb['Inventário de Processos']
print('Dimensões:', ws.dimensions)
print('Tables:', list(ws.tables))
# Confirmar que a linha 5 (exemplo) ainda está intacta
print('L5 col B:', ws.cell(row=5, column=2).value)
```

A linha 5 (exemplo "Fazer um bolo de cenoura") **deve** estar preservada.

## Tratamento de erros comuns

| Erro | Causa | Solução |
|---|---|---|
| `FileNotFoundError: asset não encontrado` | Asset não está em `assets/Modelo_Inventario_Processos.xlsx` | Verificar estrutura da skill |
| `Aba 'Inventário de Processos' não encontrada` | Arquivo base não é o modelo correto, ou aba foi renomeada | Pedir ao usuário arquivo no formato original |
| Coluna vazia inesperada no output | Nome da chave no JSON não bate com cabeçalho (ex.: "Codigo" sem acento) | Conferir nomes na lista acima |
