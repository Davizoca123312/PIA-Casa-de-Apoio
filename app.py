from flask import Flask, request, jsonify, render_template, redirect, url_for
from db import insert_user, get_user_by_cpf  # Certifique-se de que get_user_by_cpf está implementado
from user import db, User, Medicamento, Sobre, Cid  # Importando o modelo Cid
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'  # ou o banco de dados que você estiver usando
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Função para validar o CPF
def is_valid_cpf(cpf):
    cpf = cpf.replace('.', '').replace('-', '')  # Limpar CPF da formatação

    # Verifica se o CPF tem 11 caracteres e não é uma sequência de números iguais
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    # Validação do primeiro dígito verificador
    sum1 = 0
    for i in range(9):
        sum1 += int(cpf[i]) * (10 - i)
    rest1 = (sum1 * 10) % 11
    if rest1 == 10 or rest1 == 11:
        rest1 = 0
    if rest1 != int(cpf[9]):
        return False

    # Validação do segundo dígito verificador
    sum2 = 0
    for i in range(10):
        sum2 += int(cpf[i]) * (11 - i)
    rest2 = (sum2 * 10) % 11
    if rest2 == 10 or rest2 == 11:
        rest2 = 0
    if rest2 != int(cpf[10]):
        return False

    return True

# Página inicial com o login
@app.route("/", methods=["GET"])
def get0():
    return render_template("login.html")

# Rota de login (POST)
@app.route("/login", methods=["POST"])
def logar():
    cpf = request.json.get("cpf")

    if not cpf:
        return jsonify({"error": "CPF não fornecido"}), 400

    cpf = cpf.replace(".", "").replace("-", "")  # Limpeza do CPF

    if not is_valid_cpf(cpf):
        return jsonify({"error": "CPF inválido"}), 400

    # Verifica se o CPF existe no banco de dados
    user = get_user_by_cpf(cpf)
    
    if user:
        return jsonify({"message": "Login realizado com sucesso!"}), 200
    else:
        return jsonify({"error": "CPF não encontrado"}), 404

# Página principal (após login)
@app.route("/main.html", methods=["GET"])
def main_page():
    cpf = request.args.get('cpf')  # Recebe o CPF via query string

    if not cpf or not is_valid_cpf(cpf):
        return redirect(url_for('get0'))  # Se o CPF não for válido ou não for enviado, redireciona para a tela de login

    # Buscar usuário no banco de dados
    user = get_user_by_cpf(cpf)
    
    if not user:
        return redirect(url_for('get0'))  # Se o CPF não for encontrado no banco, redireciona para o login
    
    # Passa os dados do usuário para o template
    return render_template("main.html", user=user)

# Rota para registrar o novo usuário no banco de dados
@app.route('/admin/register', methods=['POST'])
def register_admin():
    cpf = request.form.get('cpf')  # Dados via FormData no Flask
    nome = request.form.get('nome')
    data_nascimento = request.form.get('data_nascimento')
    estado_civil = request.form.get('estado_civil')
    sexo = request.form.get('sexo')  # Novo campo
    nome_responsavel = request.form.get('nome_responsavel')  # Novo campo
    telefone_responsavel = request.form.get('telefone_responsavel')  # Novo campo

    # Verifica se todos os campos foram preenchidos
    if not cpf or not nome or not data_nascimento or not estado_civil:
        return jsonify({"error": "Todos os campos são obrigatórios."}), 400

    # Valida o CPF com a função is_valid_cpf
    if not is_valid_cpf(cpf):
        return jsonify({"error": "CPF inválido"}), 400

    # Tenta registrar o usuário no banco de dados
    try:
        insert_user(cpf, nome, data_nascimento, estado_civil, sexo, nome_responsavel, telefone_responsavel)
        return jsonify({"message": "Usuário cadastrado com sucesso!"}), 201
    except Exception as e:
        return jsonify({"error": f"Erro ao registrar o usuário: {e}"}), 500

# Página de registro de administrador
@app.route("/admin/register", methods=["GET"])
def admin_register():
    return render_template("admin_register.html")

# Rota para adicionar medicamento
@app.route("/add_medicamento", methods=["POST"])
def add_medicamento():
    data = request.get_json()

    nome = data.get("nome")
    horario = data.get("horario")
    periodo = data.get("periodo")
    cpf = data.get("cpf")

    if not nome or not horario or not periodo or not cpf:
        return jsonify({"error": "Todos os campos são obrigatórios."}), 400

    # Encontrar o usuário pelo CPF
    user = User.query.filter_by(cpf=cpf).first()

    if not user:
        return jsonify({"error": "Usuário não encontrado."}), 404

    # Adicionar medicamento ao banco
    novo_medicamento = Medicamento(nome=nome, horario=horario, periodo=periodo, user_id=user.id)
    db.session.add(novo_medicamento)
    db.session.commit()

    return jsonify({"message": "Medicamento adicionado com sucesso!"}), 201

@app.route("/get_medicamentos/<cpf>", methods=["GET"])
def get_medicamentos(cpf):
    user = User.query.filter_by(cpf=cpf).first()
    if not user:
        return jsonify({"error": "Usuário não encontrado."}), 404

    medicamentos = Medicamento.query.filter_by(user_id=user.id).all()
    medicamentos_list = [{"nome": m.nome, "horario": m.horario, "periodo": m.periodo} for m in medicamentos]

    return jsonify({"medicamentos": medicamentos_list}), 200

@app.route("/get_sobre/<cpf>", methods=["GET"])
def get_sobre(cpf):
    user = User.query.filter_by(cpf=cpf).first()
    if not user:
        return jsonify({"error": "Usuário não encontrado."}), 404

    sobre_info = Sobre.query.filter_by(user_id=user.id).all()
    sobre_list = [s.texto for s in sobre_info]

    return jsonify({"sobre": sobre_list}), 200

# Rota para adicionar CID
@app.route("/add_cid", methods=["POST"])
def add_cid():
    data = request.get_json()

    codigo = data.get("codigo")
    descricao = data.get("descricao")
    cpf = data.get("cpf")

    if not codigo or not descricao or not cpf:
        return jsonify({"error": "Todos os campos são obrigatórios."}), 400

    # Encontrar o usuário pelo CPF
    user = User.query.filter_by(cpf=cpf).first()

    if not user:
        return jsonify({"error": "Usuário não encontrado."}), 404

    # Adicionar CID ao banco
    novo_cid = Cid(codigo=codigo, descricao=descricao, user_id=user.id)
    db.session.add(novo_cid)
    db.session.commit()

    return jsonify({"message": "CID adicionado com sucesso!"}), 201

@app.route("/get_cids/<cpf>", methods=["GET"])
def get_cids(cpf):
    user = User.query.filter_by(cpf=cpf).first()
    if not user:
        return jsonify({"error": "Usuário não encontrado."}), 404

    cids = Cid.query.filter_by(user_id=user.id).all()
    cids_list = [{"codigo": cid.codigo, "descricao": cid.descricao} for cid in cids]

    return jsonify({"cids": cids_list}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados
    app.run(debug=True)
