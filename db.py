import sqlite3
import json

def create_table():
    """Função para criar a tabela de usuários se ela não existir."""
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    
    # Criando a tabela com as novas colunas (sexo, nome do responsável, telefone do responsável)
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cpf TEXT UNIQUE NOT NULL,
            nome TEXT NOT NULL,
            data_nascimento TEXT NOT NULL,
            estado_civil TEXT NOT NULL,
            sexo TEXT,
            nome_responsavel TEXT,
            telefone_responsavel TEXT
        )
    ''')
    
    connection.commit()
    connection.close()

def insert_user(cpf, nome, data_nascimento, estado_civil, sexo=None, nome_responsavel=None, telefone_responsavel=None):
    """Função para inserir um usuário no banco de dados."""
    try:
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        
        # Inserindo os dados do usuário na tabela 'users'
        cursor.execute(''' 
            INSERT INTO users (cpf, nome, data_nascimento, estado_civil, sexo, nome_responsavel, telefone_responsavel) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (cpf, nome, data_nascimento, estado_civil, sexo, nome_responsavel, telefone_responsavel))
        
        connection.commit()
        connection.close()
    except sqlite3.IntegrityError:
        raise ValueError("Erro: CPF já registrado!")

def get_user_by_cpf(cpf):
    """Função para verificar se o CPF existe no banco de dados e retornar o usuário."""
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    
    cursor.execute('SELECT * FROM users WHERE cpf = ?', (cpf,))
    user = cursor.fetchone()
    
    connection.close()
    
    if user:
        user_dict = {
            "id": user[0],
            "cpf": user[1],
            "nome": user[2],
            "data_nascimento": user[3],
            "estado_civil": user[4],
            "sexo": user[5],
            "nome_responsavel": user[6],
            "telefone_responsavel": user[7]
        }
        return user_dict
    return None

def get_all_users():
    """Função para retornar todos os usuários em formato JSON."""
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    
    connection.close()
    
    # Convertendo os resultados para formato JSON
    users_list = []
    for user in users:
        user_dict = {
            "id": user[0],
            "cpf": user[1],
            "nome": user[2],
            "data_nascimento": user[3],
            "estado_civil": user[4],
            "sexo": user[5],
            "nome_responsavel": user[6],
            "telefone_responsavel": user[7]
        }
        users_list.append(user_dict)
    
    return json.dumps(users_list, ensure_ascii=False)

# Criar a tabela ao iniciar o banco de dados
create_table()
