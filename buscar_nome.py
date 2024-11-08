import mysql.connector
from conexao import create_connection
import base64
from flask import Blueprint

# Defina o blueprint para buscar_nome
buscar_bp = Blueprint('buscar_bp', __name__)

# Função para converter dados binários de fotos em base64
def converter_para_base64(foto_binaria):
    if foto_binaria:
        return base64.b64encode(foto_binaria).decode('utf-8')
    return None

# Função para buscar as fotos da tabela 'fotos'
def buscar_fotos_do_cliente(cliente_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT foto1, foto2
            FROM fotos
            WHERE cliente_id = %s
        """, (cliente_id,))
        fotos = cursor.fetchone()
        return fotos if fotos else (None, None)
    except mysql.connector.Error as err:
        print(f"Erro ao buscar fotos do cliente: {err}")
        return (None, None)
    finally:
        cursor.close()
        conn.close()

# Função para buscar a foto da casa da tabela 'endereco'
def buscar_foto_casa(cliente_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT foto_casa
            FROM endereco
            WHERE cliente_id = %s
        """, (cliente_id,))
        foto_casa = cursor.fetchone()
        return foto_casa[0] if foto_casa else None
    except mysql.connector.Error as err:
        print(f"Erro ao buscar foto da casa: {err}")
        return None
    finally:
        cursor.close()
        conn.close()

# Função consolidada para obter todas as fotos
def obter_fotos_cliente(cliente_id):
    fotos_bytes = buscar_fotos_do_cliente(cliente_id)
    foto_casa_bytes = buscar_foto_casa(cliente_id)
    
    return {
        'foto1': converter_para_base64(fotos_bytes[0]) if fotos_bytes else None,
        'foto2': converter_para_base64(fotos_bytes[1]) if fotos_bytes else None,
        'foto_casa': converter_para_base64(foto_casa_bytes)
    }

# Função principal para buscar os dados do cliente
def buscar_dados_cliente(nome):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT cliente_id, nome, nome_mae, nome_pai, DATE_FORMAT(data_nasc, '%d/%m/%Y') AS data_nasc, 
                   nat, nat_uf, cpf, rg, telefone, telefone_secundario, observacao
            FROM alvo
            WHERE nome = %s
        """, (nome,))
        cliente = cursor.fetchone()
        if not cliente:
            print(f"Nenhum cliente encontrado com o nome: {nome}")
            return None

        cliente_id = cliente[0]
        
        # Buscando os dados do endereço do cliente
        cursor.execute("""
            SELECT logradouro, numero, complemento, bairro, cidade, uf, obs_endereco, foto_casa, link_endereco
            FROM endereco
            WHERE cliente_id = %s
        """, (cliente_id,))
        endereco = cursor.fetchone()

        # Obtendo as fotos do cliente
        fotos_cliente = obter_fotos_cliente(cliente_id)

        # Buscando as informações adicionais do cliente
        cursor.execute("""
            SELECT info_adicionais, nome_operacao
            FROM informacoes
            WHERE cliente_id = %s
        """, (cliente_id,))
        informacoes = cursor.fetchone()

        dados_cliente = {
            'cliente': {
                'cliente_id': cliente_id,
                'nome': cliente[1],
                'nome_mae': cliente[2],
                'nome_pai': cliente[3],
                'data_nasc': cliente[4],                
                'nat': cliente[5],
                'nat_uf': cliente[6],
                'cpf': cliente[7],
                'rg': cliente[8],
                'telefone': cliente[9],
                'telefone_secundario': cliente[10],
                'observacao': cliente[11],
            },
            'endereco': {
                'logradouro': endereco[0] if endereco else '',
                'numero': endereco[1] if endereco else '',
                'complemento': endereco[2] if endereco else '',
                'bairro': endereco[3] if endereco else '',
                'cidade': endereco[4] if endereco else '',
                'uf': endereco[5] if endereco else '',
                'obs_endereco': endereco[6] if endereco else '',
                'foto_casa': converter_para_base64(endereco[7]) if endereco else None,
                'link_endereco': endereco[8] if endereco else ''
            },
            'fotos': fotos_cliente,
            'informacoes': {
                'info_adicionais': informacoes[0] if informacoes else '',
                'nome_operacao': informacoes[1] if informacoes else ''
            }
        }
        
        return dados_cliente
    except mysql.connector.Error as err:
        print(f"Erro ao buscar dados do cliente: {err}")
        return None
    finally:
        cursor.close()
        conn.close()
