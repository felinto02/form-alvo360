from flask import Blueprint, request, redirect, url_for, flash
from conexao import create_connection
import mysql.connector

salvar_bp = Blueprint('salvar', __name__)

@salvar_bp.route('/salvar_dados', methods=['POST'])
def salvar_dados():
    try:
        # Coletando dados do formulário
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

        # Verificar se o nome já existe no banco de dados
        sql_check = "SELECT COUNT(*) FROM sua_tabela WHERE nome = %s"
        cursor.execute(sql_check, (nome,))
        resultado = cursor.fetchone()

        if resultado[0] > 0:
            # Se o nome já existir, exibe uma mensagem de erro
            flash(f"O nome '{nome}' já existe no banco de dados.", "erro")
            return redirect(url_for('index'))  # Redireciona de volta ao formulário

        # Comando SQL para inserir dados na tabela (ajuste o nome da tabela e colunas conforme necessário)
        sql = """
            INSERT INTO sua_tabela (nome_operacao, nome, nome_mae, nome_pai, data_nasc, nat, nat_uf, cpf, rg, telefone,
                                    telefone_secundario, observacao, logradouro, numero, complemento, bairro,
                                    cidade, uf_endereco, obs_endereco, link_endereco, informacoes_adicionais,
                                    foto1, foto2, foto_casa) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Prepare os dados para o SQL
        dados = (nome_operacao, nome, nome_mae, nome_pai, data_nasc, nat, nat_uf, cpf, rg, telefone,
                 telefone_secundario, observacao, logradouro, numero, complemento, bairro,
                 cidade, uf_endereco, obs_endereco, link_endereco, informacoes_adicionais,
                 foto1.read() if foto1 else None,
                 foto2.read() if foto2 else None,
                 foto_casa.read() if foto_casa else None)

        # Executa o comando SQL
        cursor.execute(sql, dados)
        conexao.commit()

        flash('Dados salvos com sucesso!', 'sucesso')
        return redirect(url_for('index'))  # Redireciona para a rota do index

    except mysql.connector.Error as erro:
        print(f"Erro ao salvar os dados: {erro}")
        conexao.rollback()
        flash('Erro ao salvar os dados. Tente novamente.', 'erro')
        return redirect(url_for('index'))  # Redireciona para a rota do index

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()
