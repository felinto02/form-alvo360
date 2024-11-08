from flask import Flask, request, jsonify, render_template, flash, Blueprint, send_file
from buscar_nome import buscar_dados_cliente, obter_fotos_cliente, buscar_bp
from salvar import salvar_bp
from editar import editar_bp
from conexao import create_connection, close_connection
from flask import Flask, send_file, request
from folha_info import gerar_pdf_qrcode
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)

# Configuração do Flask usando DATABASE_URL
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

# Registre os blueprints
app.register_blueprint(salvar_bp)
app.register_blueprint(buscar_bp)
app.register_blueprint(editar_bp)



@app.route('/gerar_qrcode_pdf/<int:cliente_id>', methods=['GET'])
def gerar_qrcode_pdf(cliente_id):
    # Gera o PDF com o QR Code usando o cliente_id
    pdf_buffer = gerar_pdf_qrcode(cliente_id)

    # Retorna o PDF gerado como resposta
    return send_file(pdf_buffer, as_attachment=True, download_name=f"qrcode_cliente_{cliente_id}.pdf", mimetype='application/pdf')


@app.route('/suggest_names', methods=['GET'])
def suggest_names():
    nome_parcial = request.args.get('query', '')
    
    conexao = create_connection()
    if conexao:
        cursor = conexao.cursor(dictionary=True)
        query = "SELECT nome FROM alvo WHERE nome LIKE %s LIMIT 10"
        cursor.execute(query, (f'%{nome_parcial}%',))
        resultados = cursor.fetchall()
        cursor.close()
        close_connection(conexao)
        
        sugestoes = [resultado['nome'] for resultado in resultados]
        return jsonify(sugestoes)
    
    return jsonify([])  # Retorna uma lista vazia se houver um erro na conexão


@app.route('/buscar_dados_cliente', methods=['GET'])
def buscar_dados_cliente_route():
    nome = request.args.get('nome')
    cliente = buscar_dados_cliente(nome)
        
    if cliente:
        fotos_base64 = obter_fotos_cliente(cliente['cliente']['cliente_id'])
        cliente['fotos'] = fotos_base64  # Adiciona as fotos em base64
        return jsonify(cliente)

    return jsonify({"error": "Cliente não encontrado"}), 404


@app.route('/')
def index():
    conexao = create_connection()
    
    if conexao:
        try:
            # Chama a função buscar_dados_cliente, que você já tem, para buscar os dados do cliente
            dados = buscar_dados_cliente(conexao)  # Função já existente
        except Exception as e:
            #flash(f"Erro ao buscar dados: {str(e)}", "error")
            dados = {}  # Se houver erro, `dados` será um dicionário vazio
        finally:
            close_connection(conexao)  # Certifique-se de desconectar após terminar o uso

        return render_template('formulario.html', dados=dados)
    
    else:
        flash("Erro ao conectar ao banco de dados. O servidor pode estar fora do ar.", "error")
        return render_template('formulario.html', dados={})


if __name__ == '__main__':
    app.run(debug=True)
