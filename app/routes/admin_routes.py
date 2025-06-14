from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app.models.user_model import db, User
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

admin_routes = Blueprint('admin', __name__)

# Configurações de e-mail (direto no código)
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USER = ''  # Seu e-mail
EMAIL_PASS = ''       # Senha fornecida (troque após o teste)
EMAIL_TO = ''    # E-mail que receberá o alerta

# Função para enviar e-mail de alerta
def notify_admin_email(ip):
    if not (EMAIL_USER and EMAIL_PASS and EMAIL_TO):
        print('E-mail não configurado corretamente.')
        return
    subject = 'Tentativa de acesso à página de logins (admin)'
    body = f"Tentativa de acesso à página de logins. IP: {ip}. Permitir acesso?"
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_TO
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
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
    autorizado = session.get('admin_logins_autorizado')
    if not autorizado:
        notify_admin_email(user_ip)
        flash('Aguardando autorização do administrador para acessar esta página.')
        return render_template('aguardando_autorizacao.html', ip=user_ip)
    users = User.query.all()
    return render_template('admin_logins.html', users=users)

# Rota para liberar acesso (simulação, pode ser via link enviado no e-mail)
@admin_routes.route('/admin/autorizar_logins')
def autorizar_logins():
    session['admin_logins_autorizado'] = True
    flash('Acesso liberado!')
    return redirect(url_for('admin.admin_logins'))
