from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from app.models.user_model import db, User
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import uuid

admin_routes = Blueprint('admin', __name__)

# Controle de autorizações por token (em memória)
pending_auths = {}

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USER = 'fornute3@gmail.com'
EMAIL_PASS = 'rpny eeph muzr blow'
EMAIL_TO = 'fornute3@gmail.com'

# URL da logo (pode trocar por uma imagem do seu projeto)
LOGO_URL = 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/React-icon.svg/512px-React-icon.svg.png'

# Função para enviar e-mail de alerta profissional
def notify_admin_email(ip, token):
    if not (EMAIL_USER and EMAIL_PASS and EMAIL_TO):
        print('E-mail não configurado corretamente.')
        return
    subject = 'Tentativa de acesso à página de logins (admin)'
    now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    # Link para autorizar (ajuste o domínio se não for localhost)
    autorizar_url = f"http://localhost:5000/admin/autorizar_logins?token={token}"
    html = f'''
    <div style="font-family:Arial,sans-serif;max-width:500px;margin:auto;border:1px solid #eee;border-radius:8px;box-shadow:0 2px 8px #ccc;padding:32px 24px;background:#fafbfc;">
        <div style="text-align:center;margin-bottom:24px;">
            <img src="{LOGO_URL}" alt="Logo" style="width:80px;height:80px;">
        </div>
        <h2 style="color:#2c3e50;text-align:center;">Alerta de Tentativa de Acesso</h2>
        <p style="font-size:1.1em;color:#333;">Detectamos uma tentativa de acesso à <b>página de logins de administrador</b> no sistema <b>Casa de Apoio</b>.</p>
        <ul style="font-size:1em;color:#555;">
            <li><b>IP:</b> {ip}</li>
            <li><b>Data/Hora:</b> {now}</li>
        </ul>
        <p style="margin:24px 0 16px 0;text-align:center;">
            <a href="{autorizar_url}" style="background:#3498db;color:#fff;padding:14px 32px;border-radius:6px;text-decoration:none;font-weight:bold;font-size:1.1em;">Permitir acesso</a>
        </p>
        <p style="color:#888;font-size:0.95em;text-align:center;">Se não foi você, ignore este e-mail.</p>
    </div>
    '''
    msg = MIMEMultipart('alternative')
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_TO
    msg['Subject'] = subject
    msg.attach(MIMEText(html, 'html'))
    try:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, EMAIL_TO, msg.as_string())
        server.quit()
    except Exception as e:
        print(f'Erro ao enviar e-mail: {e}')

# Rota protegida para visualizar logins
@admin_routes.route('/admin/logins')
def admin_logins():
    user_ip = request.remote_addr
    token = session.get('auth_token')
    # Se já existe token e está autorizado, mostra a página de logins
    if token and pending_auths.get(token):
        users = User.query.all()
        return render_template('admin_logins.html', users=users)
    # Se não, gera novo token e inicia fluxo de autorização
    token = str(uuid.uuid4())
    session['auth_token'] = token
    pending_auths[token] = False
    notify_admin_email(user_ip, token)
    flash('Aguardando autorização do administrador para acessar esta página.')
    return render_template('aguardando_autorizacao.html', ip=user_ip, token=token)

# Rota para liberar acesso (simulação, pode ser via link enviado no e-mail)
@admin_routes.route('/admin/autorizar_logins')
def autorizar_logins():
    token = request.args.get('token')
    if token and token in pending_auths:
        pending_auths[token] = True
        return '<h2>Acesso liberado para o usuário!</h2><p>Você pode fechar esta janela.</p>'
    return '<h2>Token inválido ou já autorizado.</h2>'

# Endpoint para polling AJAX
@admin_routes.route('/admin/check_autorizacao', methods=['POST'])
def check_autorizacao():
    data = request.get_json()
    token = data.get('token')
    autorizado = pending_auths.get(token, False)
    return jsonify({'autorizado': bool(autorizado)})
