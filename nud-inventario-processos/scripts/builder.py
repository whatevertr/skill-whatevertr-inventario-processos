"""
Builder do Inventário de Processos.

Preserva 100% da estrutura visual do modelo (Excel Table, cores, freeze,
linha 4 de instrução, linha 5 de exemplo) e apenas insere/atualiza linhas
de dados a partir da linha 6.

Modos:
- NOVO: parte do asset assets/Modelo_Inventario_Processos.xlsx
- INCREMENTO: parte do arquivo existente passado em --base e continua
  a numeração após a última linha preenchida.

Uso:
    python builder.py --output saida.xlsx --linhas linhas.json
    python builder.py --base existente.xlsx --output saida.xlsx --linhas linhas.json

Formato do JSON de linhas (lista de dicts, uma chave por coluna):
[
  {
    "Nome do Processo": "Fazer um bolo de cenoura",
    "Gatilho": "Por demanda — pedido de encomenda",
    ...
    "Legislação Aplicável": [{"texto": "Boas práticas (RDC Anvisa)", "origem": "inferido"}],
    "Riscos": [
        {"id": "R01", "texto": "Qualidade: fermento vencido não cresce", "origem": "inferido"},
        {"id": "R02", "texto": "Prazo: forno ocupado atrasa a entrega", "origem": "inferido", "importante": true}
    ],
    "Oportunidades": [{"id": "O01", "texto": "Padronizar em ficha técnica", "origem": "inferido"}],
    "Comentários": "Itens em laranja são inferência da skill; 🍷 = repetição de ID inferida — validar."
  },
  ...
]

CONVENÇÃO DE COR (campos Legislação, Riscos, Oportunidades):
- Cada item pode ser um dict {"texto", "origem": "inferido"|"literal", "importante": bool, "id": "R01"} OU
  uma string simples (tratada como literal grafite).
- origem "inferido" → texto LARANJA · origem "literal" + importante → VIOLETA NEGRITO ·
  literal normal → grafite. importante + inferido → LARANJA NEGRITO.
- Riscos/Oportunidades: o "id" (R01/O01) é atribuído pelo Claude (contínuo no inventário,
  reusado em repetições com 🍷) — o builder só renderiza; não renumera.

Código/N° NÃO precisa estar no JSON — o builder calcula automaticamente (E01, E02...).
"""

import argparse
import json
import os
import shutil
import sys
from copy import copy
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.cell.rich_text import CellRichText, TextBlock
from openpyxl.cell.text import InlineFont

# Convenção de cor — paleta NUD (dia). O NUD não tem vermelho.
COR_INFERIDO = '993700'   # laranja NUD — inferência da skill (o que validar)
COR_LITERAL_IMP = '642DA4'  # violeta NUD — literal importante (ênfase)
COR_PADRAO = '191128'     # grafite NUD — literal normal (tinta, nunca preto puro)
PREFIXO_ETAPA = 'E'       # E01, E02...

# Campos que recebem cor por origem
CAMPOS_COLORIDOS = ('Legislação Aplicável', 'Riscos', 'Oportunidades')


def _inline(item):
    """Define a InlineFont de um item conforme origem + importância."""
    origem = item.get('origem', 'literal')
    imp = bool(item.get('importante'))
    if origem == 'inferido':
        return InlineFont(rFont='Consolas', sz=10, color=COR_INFERIDO, b=imp)
    if imp:  # literal importante
        return InlineFont(rFont='Consolas', sz=10, color=COR_LITERAL_IMP, b=True)
    return InlineFont(rFont='Consolas', sz=10, color=COR_PADRAO, b=False)


def _rich(valor):
    """Converte o valor de um campo colorido em CellRichText.
    Aceita string simples (literal grafite) ou lista de itens (dict/str)."""
    if valor is None or valor == '':
        return None
    if isinstance(valor, str):
        return valor  # texto simples, cor padrão da célula
    itens = valor if isinstance(valor, list) else [valor]
    blocos = []
    for i, it in enumerate(itens):
        if isinstance(it, str):
            it = {'texto': it, 'origem': 'literal'}
        prefixo = (it['id'] + '  ') if it.get('id') else ''
        texto = prefixo + it.get('texto', '')
        if i < len(itens) - 1:
            texto += '\n'
        blocos.append(TextBlock(_inline(it), texto))
    return CellRichText(*blocos)

# Ordem das colunas no modelo (linha 3 do .xlsx)
COLUNAS = [
    'Código/N°',
    'Nome do Processo',
    'Gatilho',
    'Fornecedor (S)',
    'Entrada (I)',
    'Processo (P)',
    'Responsável',
    'Saída (O)',
    'Cliente (C)',
    'SLA',
    'Indicador',
    'Sistemas / Recursos',
    'Legislação Aplicável',
    'Riscos',
    'Oportunidades',
    'Comentários',
]

# Estilos padronizados (espelham o modelo)
BLANK_FILL = PatternFill('solid', start_color='E7DCD0')  # papel NUD (linha a preencher)
BODY_FONT = Font(name='Consolas', size=10)               # mono NUD
THIN = Side(border_style='thin', color='ABA9B3')         # rule NUD
BORDER_ALL = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

# Constantes de layout (linhas fixas do modelo)
LINHA_HEADER = 3
LINHA_INSTRUCAO = 4
LINHA_EXEMPLO = 5
PRIMEIRA_LINHA_DADOS = 6  # daqui pra baixo são linhas a preencher

NOME_ABA = 'Inventário de Processos'
NOME_TABELA = 'InventarioProcessos'


def _asset_path():
    """Resolve o caminho do asset relativo a este script."""
    aqui = Path(__file__).resolve().parent
    candidato = aqui.parent / 'assets' / 'Modelo_Inventario_Processos.xlsx'
    if candidato.exists():
        return str(candidato)
    raise FileNotFoundError(
        f'Asset não encontrado: {candidato}. '
        'O arquivo Modelo_Inventario_Processos.xlsx deve estar em assets/.'
    )


def _proxima_linha_vazia(ws):
    """Retorna a primeira linha sem 'Nome do Processo' (coluna B) preenchido,
    começando a partir de PRIMEIRA_LINHA_DADOS."""
    r = PRIMEIRA_LINHA_DADOS
    while ws.cell(row=r, column=2).value is not None and r < 10000:
        r += 1
    return r


def _ultimo_codigo(ws):
    """Retorna o maior número usado na coluna A (Código/N°) a partir de L6.
    Considera apenas linhas que tenham conteúdo na coluna B (Nome do Processo)
    — isso evita contar números pré-populados sem dados reais."""
    import re
    maior = 0
    for r in range(PRIMEIRA_LINHA_DADOS, ws.max_row + 1):
        nome = ws.cell(row=r, column=2).value
        cod = ws.cell(row=r, column=1).value
        if nome is None:
            continue
        if isinstance(cod, (int, float)):
            maior = max(maior, int(cod))
        elif isinstance(cod, str):
            m = re.search(r'(\d+)\s*$', cod)  # pega o número no fim (E01, DEV-01...)
            if m:
                maior = max(maior, int(m.group(1)))
    return maior


def _aplicar_estilo_linha(ws, linha):
    """Aplica fonte/alinhamento/borda padrão e remove fill laranja (a linha
    deixa de ser 'a preencher' quando é preenchida)."""
    for c in range(1, len(COLUNAS) + 1):
        cell = ws.cell(row=linha, column=c)
        cell.font = BODY_FONT
        cell.alignment = Alignment(vertical='top', wrap_text=True)
        cell.border = BORDER_ALL
        # Remove o fill laranja claro (a linha agora tem dados)
        cell.fill = PatternFill(fill_type=None)
    ws.row_dimensions[linha].height = 60


def _inserir_linha_em_branco_se_necessario(ws, linha):
    """Garante que a linha existe com formatação base (laranja claro).
    Útil quando precisamos escrever em linhas que não foram pré-criadas."""
    for c in range(1, len(COLUNAS) + 1):
        cell = ws.cell(row=linha, column=c)
        if cell.value is None and cell.fill.start_color.rgb in (None, '00000000'):
            cell.fill = BLANK_FILL
            cell.font = BODY_FONT
            cell.alignment = Alignment(vertical='top', wrap_text=True)
            cell.border = BORDER_ALL


def _atualizar_ref_tabela(ws, ultima_linha):
    """Atualiza o ref do Excel Table para abranger até a última linha
    preenchida. Sem isso, filtros/ordenação só funcionam até o ref antigo."""
    tabela = None
    for nome_tbl in list(ws.tables):
        if nome_tbl == NOME_TABELA:
            tabela = ws.tables[nome_tbl]
            break
    if tabela is None:
        # Tabela ausente — recriar
        last_col = get_column_letter(len(COLUNAS))
        ref = f'A{LINHA_HEADER}:{last_col}{ultima_linha}'
        nova = Table(displayName=NOME_TABELA, ref=ref)
        nova.tableStyleInfo = TableStyleInfo(
            name='TableStyleMedium2',
            showFirstColumn=False, showLastColumn=False,
            showRowStripes=False, showColumnStripes=False,
        )
        ws.add_table(nova)
        return

    last_col = get_column_letter(len(COLUNAS))
    novo_ref = f'A{LINHA_HEADER}:{last_col}{ultima_linha}'
    tabela.ref = novo_ref


def construir(base_path, output_path, linhas):
    """
    base_path : caminho do .xlsx base (asset ou existente).
    output_path: onde salvar.
    linhas    : lista de dicts (uma por processo). Código/N° é auto.
    """
    # Cópia para não mexer no arquivo base
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    shutil.copy(base_path, output_path)

    wb = load_workbook(output_path)
    if NOME_ABA not in wb.sheetnames:
        raise ValueError(
            f"Aba '{NOME_ABA}' não encontrada no arquivo base. "
            f"Abas presentes: {wb.sheetnames}"
        )
    ws = wb[NOME_ABA]

    # Decide próxima linha disponível
    linha_destino = _proxima_linha_vazia(ws)
    proximo_codigo = _ultimo_codigo(ws) + 1

    for registro in linhas:
        _inserir_linha_em_branco_se_necessario(ws, linha_destino)

        # Código automático (coluna 1) — E01, E02...
        ws.cell(row=linha_destino, column=1).value = f'{PREFIXO_ETAPA}{proximo_codigo:02d}'

        # Demais colunas — só escreve se houver chave no dict
        for c, nome_col in enumerate(COLUNAS[1:], start=2):
            valor = registro.get(nome_col)
            if valor is None or valor == '':
                continue
            if nome_col in CAMPOS_COLORIDOS:
                ws.cell(row=linha_destino, column=c).value = _rich(valor)
            else:
                ws.cell(row=linha_destino, column=c).value = valor

        _aplicar_estilo_linha(ws, linha_destino)
        linha_destino += 1
        proximo_codigo += 1

    # Atualiza ref da Excel Table
    ultima_linha = linha_destino - 1
    _atualizar_ref_tabela(ws, ultima_linha)

    wb.save(output_path)

    # Check de cor pós-build: se havia item inferido nos dados mas o .xlsx
    # saiu sem nenhum texto colorido, a rastreabilidade se perdeu (falha).
    alerta = _verificar_cor(output_path, linhas)
    if alerta:
        print(alerta, file=sys.stderr)


def _verificar_cor(output_path, linhas):
    """Retorna string de alerta se há origem 'inferido' nos dados de entrada
    mas 0 blocos rich-text coloridos no arquivo salvo. Vazio = ok."""
    tem_inferido = False
    for reg in linhas:
        for campo in CAMPOS_COLORIDOS:
            val = reg.get(campo)
            itens = val if isinstance(val, list) else ([val] if val else [])
            for it in itens:
                if isinstance(it, dict) and it.get('origem') == 'inferido':
                    tem_inferido = True
    if not tem_inferido:
        return ''
    wb = load_workbook(output_path, rich_text=True)
    ws = wb[NOME_ABA]
    for row in ws.iter_rows():
        for cell in row:
            if isinstance(cell.value, CellRichText):
                for blk in cell.value:
                    cor = getattr(getattr(blk, 'font', None), 'color', None)
                    rgb = getattr(cor, 'rgb', None) or ''
                    if isinstance(blk, TextBlock) and rgb[-6:].upper() == COR_INFERIDO:
                        return ''  # achou o LARANJA dos inferidos: ok
    return ('ALERTA DE COR: havia itens inferidos, mas o .xlsx saiu sem o LARANJA '
            f'(#{COR_INFERIDO}) da inferencia. A distincao literal x inferido se '
            'perdeu — revise o build antes de entregar.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--base',
        help='Caminho do .xlsx existente para incrementar. '
             'Se omitido, usa o asset (modo NOVO).'
    )
    parser.add_argument(
        '--output',
        required=True,
        help='Caminho do .xlsx de saída.'
    )
    parser.add_argument(
        '--linhas',
        required=True,
        help='Caminho do JSON com a lista de linhas a inserir, OU '
             "string JSON inline (ex.: '[{\"Nome do Processo\": \"...\"}]')."
    )
    args = parser.parse_args()

    base = args.base if args.base else _asset_path()

    # Aceita arquivo OU string JSON inline
    if args.linhas.strip().startswith('['):
        linhas = json.loads(args.linhas)
    else:
        with open(args.linhas, 'r', encoding='utf-8') as f:
            linhas = json.load(f)

    if not isinstance(linhas, list):
        print('ERRO: --linhas deve ser uma lista (JSON array).', file=sys.stderr)
        sys.exit(1)

    construir(base, args.output, linhas)
    print(f'OK: {len(linhas)} linha(s) inserida(s) em {args.output}')


if __name__ == '__main__':
    main()
