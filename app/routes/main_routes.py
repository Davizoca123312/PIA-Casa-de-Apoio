# Rotas principais da aplicação
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from app.models.user_model import db, User, Medicamento, Sobre, Cid
from app.utils_cpf import is_valid_cpf
from app.routes.admin_routes import notify_admin_email, pending_auths
import uuid

main_routes = Blueprint('main', __name__)

# Página inicial com o login
@main_routes.route("/", methods=["GET"])
def get0():
    return render_template("login.html")

# Rota de login (POST)
@main_routes.route("/login", methods=["POST"])
def logar():
    cpf = request.json.get("cpf")
    if not cpf:
        return jsonify({"error": "CPF não fornecido"}), 400
    cpf = cpf.replace(".", "").replace("-", "")
    if not is_valid_cpf(cpf):
        return jsonify({"error": "CPF inválido"}), 400
    user = User.query.filter_by(cpf=cpf).first()
    if user:
        return jsonify({"message": "Login realizado com sucesso!"}), 200
    else:
        return jsonify({"error": "CPF não encontrado"}), 404

# Página principal (após login)
@main_routes.route("/main.html", methods=["GET"])
def main_page():
    cpf = request.args.get('cpf')
    if not cpf or not is_valid_cpf(cpf):
        return redirect(url_for('main.get0'))
    user = User.query.filter_by(cpf=cpf).first()
    if not user:
        return redirect(url_for('main.get0'))
    return render_template("main.html", user=user)

# Rota para registrar o novo usuário no banco de dados
@main_routes.route('/admin/register', methods=['POST'])
def register_admin():
    cpf = request.form.get('cpf')
    nome = request.form.get('nome')
    data_nascimento = request.form.get('data_nascimento')
    estado_civil = request.form.get('estado_civil')
    sexo = request.form.get('sexo')
    nome_responsavel = request.form.get('nome_responsavel')
    telefone_responsavel = request.form.get('telefone_responsavel')
    if not cpf or not nome or not data_nascimento or not estado_civil:
        return jsonify({"error": "Todos os campos são obrigatórios."}), 400
    if not is_valid_cpf(cpf):
        return jsonify({"error": "CPF inválido"}), 400
    try:
        novo_user = User(
            cpf=cpf,
            nome=nome,
            data_nascimento=data_nascimento,
            estado_civil=estado_civil,
            sexo=sexo,
            nome_responsavel=nome_responsavel,
            telefone_responsavel=telefone_responsavel
        )
        db.session.add(novo_user)
        db.session.commit()
        return jsonify({"message": "Usuário cadastrado com sucesso!"}), 201
    except Exception as e:
        return jsonify({"error": f"Erro ao registrar o usuário: {e}"}), 500

# Página de registro de administrador
@main_routes.route("/admin/register", methods=["GET"])
def admin_register():
    # Lógica de autorização por e-mail igual à de /admin/logins
    user_ip = request.remote_addr
    token = str(uuid.uuid4())
    session['auth_token_register'] = token
    pending_auths[token] = False
    notify_admin_email(user_ip, token)
    return render_template("aguardando_autorizacao.html", ip=user_ip, token=token)

# Rota para adicionar medicamento
@main_routes.route("/add_medicamento", methods=["POST"])
def add_medicamento():
    data = request.get_json()
    nome = data.get("nome")
    horario = data.get("horario")
    periodo = data.get("periodo")
    cpf = data.get("cpf")
    if not nome or not horario or not periodo or not cpf:
        return jsonify({"error": "Todos os campos são obrigatórios."}), 400
    user = User.query.filter_by(cpf=cpf).first()
    if not user:
        return jsonify({"error": "Usuário não encontrado."}), 404
    novo_medicamento = Medicamento(nome=nome, horario=horario, periodo=periodo, user_id=user.id)
    db.session.add(novo_medicamento)
    db.session.commit()
    return jsonify({"message": "Medicamento adicionado com sucesso!"}), 201

@main_routes.route("/get_medicamentos/<cpf>", methods=["GET"])
def get_medicamentos(cpf):
    user = User.query.filter_by(cpf=cpf).first()
    if not user:
        return jsonify({"error": "Usuário não encontrado."}), 404
    medicamentos = Medicamento.query.filter_by(user_id=user.id).all()
    medicamentos_list = [{"nome": m.nome, "horario": m.horario, "periodo": m.periodo} for m in medicamentos]
    return jsonify({"medicamentos": medicamentos_list}), 200

@main_routes.route("/get_sobre/<cpf>", methods=["GET"])
def get_sobre(cpf):
    user = User.query.filter_by(cpf=cpf).first()
    if not user:
        return jsonify({"error": "Usuário não encontrado."}), 404
    sobre_info = Sobre.query.filter_by(user_id=user.id).all()
    sobre_list = [s.texto for s in sobre_info]
    return jsonify({"sobre": sobre_list}), 200

# Rota para adicionar CID
@main_routes.route("/add_cid", methods=["POST"])
def add_cid():
    data = request.get_json()
    codigo = data.get("codigo")
    descricao = data.get("descricao")
    cpf = data.get("cpf")
    if not codigo or not descricao or not cpf:
        return jsonify({"error": "Todos os campos são obrigatórios."}), 400
    user = User.query.filter_by(cpf=cpf).first()
    if not user:
        return jsonify({"error": "Usuário não encontrado."}), 404
    novo_cid = Cid(codigo=codigo, descricao=descricao, user_id=user.id)
    db.session.add(novo_cid)
    db.session.commit()
    return jsonify({"message": "CID adicionado com sucesso!"}), 201

@main_routes.route("/get_cids/<cpf>", methods=["GET"])
def get_cids(cpf):
    user = User.query.filter_by(cpf=cpf).first()
    if not user:
        return jsonify({"error": "Usuário não encontrado."}), 404
    cids = Cid.query.filter_by(user_id=user.id).all()
    cids_list = [{"codigo": cid.codigo, "descricao": cid.descricao} for cid in cids]
    return jsonify({"cids": cids_list}), 200
