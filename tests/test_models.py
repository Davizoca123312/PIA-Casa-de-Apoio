from app.models.user_model import User, db

def test_user_model(app):
    with app.app_context():
        db.create_all()
        User.query.delete()  # Limpa a tabela antes do teste
        db.session.commit()
        user = User(nome="Teste", cpf="12345678901", data_nascimento="01/01/2000", estado_civil="Solteiro")
        db.session.add(user)
        db.session.commit()
        found = User.query.filter_by(cpf="12345678901").first()
        assert found is not None
        assert found.nome == "Teste"
