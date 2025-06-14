# PIA Casa de Apoio

Sistema web desenvolvido para gerenciar pacientes, medicamentos, diagnósticos (CID) e informações administrativas de uma Casa de Apoio.

## Visão Geral
O sistema permite o cadastro, consulta e gerenciamento de pacientes, seus medicamentos, diagnósticos médicos (CID) e informações complementares. Possui autenticação por CPF, interface web responsiva e integra banco de dados relacional.

## Principais Funcionalidades
- **Login seguro:** Autenticação de usuários por CPF, com validação e busca no banco de dados.
- **Cadastro de pacientes:** Registro de novos pacientes com dados pessoais, responsável e contato.
- **Gestão de medicamentos:** Adição, consulta e listagem de medicamentos vinculados a cada paciente.
- **Gestão de CID:** Cadastro e consulta de diagnósticos médicos (CID) por paciente.
- **Informações complementares:** Registro de observações e histórico do paciente.
- **Interface web:** Telas de login, cadastro e painel principal com navegação intuitiva.
- **Testes automatizados:** Cobertura de rotas e modelos para garantir a estabilidade do sistema.

## Estrutura do Projeto
```
PIA-Casa-de-Apoio/
├── app/
│   ├── models/         # Modelos de dados (ORM SQLAlchemy)
│   └── routes/         # Rotas (Blueprint Flask)
├── templates/          # Templates HTML (Jinja2)
├── tests/              # Testes automatizados (pytest)
├── main.py             # Ponto de entrada da aplicação
├── database.py         # Integração com banco SQLite e funções utilitárias
├── db.py               # Funções de manipulação direta do banco SQLite
├── requirements.txt    # Dependências do projeto
├── Procfile            # Arquivo para deploy (Heroku/Render)
├── .gitignore          # Arquivos e pastas ignorados pelo Git
```

## Como Funciona
1. **Login:** O usuário acessa a tela inicial e faz login informando o CPF. O sistema valida o CPF e busca o usuário no banco.
2. **Cadastro:** Novos pacientes podem ser cadastrados via formulário, preenchendo dados pessoais e do responsável.
3. **Painel principal:** Após login, o usuário acessa o painel com informações do paciente, medicamentos, CID e histórico.
4. **Medicamentos e CID:** É possível adicionar, consultar e listar medicamentos e diagnósticos vinculados ao paciente.
5. **Testes:** O sistema possui testes automatizados para rotas e modelos, garantindo que as principais funcionalidades estejam sempre funcionando.

## Como Executar Localmente
1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Execute a aplicação:
   ```bash
   python main.py
   ```
3. Acesse no navegador: [http://localhost:5000](http://localhost:5000)

## Como Rodar os Testes
```bash
pytest
```

## Tecnologias Utilizadas
- Python 3
- Flask (web framework)
- SQLAlchemy (ORM)
- SQLite (banco de dados)
- Pytest (testes automatizados)
- HTML5, CSS3 (templates)

## Deploy
O projeto está pronto para deploy em plataformas como Heroku ou Render, utilizando o `Procfile` e o `requirements.txt`.

## Contribuição
Pull requests são bem-vindos! Sinta-se à vontade para propor melhorias, correções ou novas funcionalidades.

---

> Projeto acadêmico desenvolvido para a disciplina de Projeto Integrador de Aplicações (PIA) - Casa de Apoio.
