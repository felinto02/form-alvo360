from flask import Blueprint, request, redirect, url_for, flash
from conexao import create_connection
import mysql.connector

editar_bp = Blueprint('editar', __name__)

@editar_bp.route('/editar_dados', methods=['POST'])
def editar_dados():
    try:
        # Coletando o ID do cliente e os dados do formulário
        cliente_id = request.form.get('cliente_id')  # Supondo que você tenha o campo hidden para o ID
        nome_operacao = request.form.get('nome_operacao')
        nome = request.form.get('nome')
        nome_mae = request.form.get('nome_mae')
        nome_pai = request.form.get('nome_pai')
        data_nasc = request.form.get('data_nasc')
        nat = request.form.get('nat')
        nat_uf = request.form.get('nat_uf')
        cpf = request.form.get('cpf')
        rg = request.form.get('rg')
        telefone = request.form.get('telefone')
        telefone_secundario = request.form.get('telefone_secundario')
        observacao = request.form.get('observacao')
        logradouro = request.form.get('logradouro')
        numero = request.form.get('numero')
        complemento = request.form.get('complemento')
        bairro = request.form.get('bairro')
        cidade = request.form.get('cidade')
        uf_endereco = request.form.get('uf_endereco')
        obs_endereco = request.form.get('obs_endereco')
        link_endereco = request.form.get('link_endereco')
        informacoes_adicionais = request.form.get('informacoes_adicionais')

        # Para os uploads de imagem
        foto1 = request.files.get('foto1')
        foto2 = request.files.get('foto2')
        foto_casa = request.files.get('foto_casa')

        # Conectar ao banco de dados
        conexao = create_connection()
        cursor = conexao.cursor()

        # Comando SQL para atualizar os dados do cliente
        sql_update = """
            UPDATE sua_tabela SET 
                nome_operacao = %s, nome = %s, nome_mae = %s, nome_pai = %s, data_nasc = %s, nat = %s, nat_uf = %s, 
                cpf = %s, rg = %s, telefone = %s, telefone_secundario = %s, observacao = %s, logradouro = %s, 
                numero = %s, complemento = %s, bairro = %s, cidade = %s, uf_endereco = %s, obs_endereco = %s, 
                link_endereco = %s, informacoes_adicionais = %s, foto1 = %s, foto2 = %s, foto_casa = %s 
            WHERE cliente_id = %s
        """

        # Dados que serão usados no UPDATE
        dados = (
            nome_operacao, nome, nome_mae, nome_pai, data_nasc, nat, nat_uf, cpf, rg, telefone,
            telefone_secundario, observacao, logradouro, numero, complemento, bairro,
            cidade, uf_endereco, obs_endereco, link_endereco, informacoes_adicionais,
            foto1.read() if foto1 else None,
            foto2.read() if foto2 else None,
            foto_casa.read() if foto_casa else None,
            cliente_id  # Adiciona o ID do cliente no final
        )

        # Executa o comando SQL de atualização
        cursor.execute(sql_update, dados)
        conexao.commit()

        # Mensagem de sucesso
        flash('Dados atualizados com sucesso!', 'sucesso')
        return redirect(url_for('index'))  # Redireciona de volta ao index

    except mysql.connector.Error as erro:
        print(f"Erro ao atualizar os dados: {erro}")
        conexao.rollback()
        flash('Erro ao atualizar os dados. Tente novamente.', 'erro')
        return redirect(url_for('index'))  # Redireciona para a rota do index

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()
