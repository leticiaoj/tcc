from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- CONFIGURAÇÃO INICIAL ---
base_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=base_dir, static_folder=base_dir, static_url_path='')
app.secret_key = "cyber_chase_secret_key"

# --- BANCO DE DADOS (MYSQL) ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@127.0.0.1:3306/cyber_chase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- MODELOS ---
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)

class Curso(db.Model):
    __tablename__ = 'cursos'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    conteudo = db.Column(db.Text, nullable=True)
    link = db.Column(db.String(100), nullable=True)

with app.app_context():
    db.create_all()

# --- INTELIGÊNCIA DO CHATBOT (MACHINE LEARNING) ---
# Base de conhecimento: Pergunta -> Resposta
conhecimento = {
    "O que é a Cyber Chase?": "A Cyber Chase é uma organização focada em educação cibernética gratuita para ajudar você a construir seu escudo digital.",
    "Quais os benefícios da plataforma?": "Além de aprender a se proteger, você turbina seu currículo com nossos certificados de conclusão!",
    "Como funcionam os cursos?": "Nossos cursos são divididos em trilhas de aprendizado com testes para validar seu conhecimento.",
    "Quem é o Cybot?": "Eu sou o Cybot, seu assistente virtual e guardião da Cyber Chase!",
    "Como posso me proteger de ataques?": "Recomendamos o uso de senhas fortes, autenticação em dois fatores (2FA) e muita atenção a links suspeitos.",
    "A plataforma emite certificado?": "Sim! Ao concluir nossos cursos e passar nos testes, você recebe um certificado da Cyber Chase.",
    "Como entrar em contato?": "Você pode acessar nossa página de Contato no menu superior para falar com o time."
}

perguntas_treino = list(conhecimento.keys())
respostas_treino = list(conhecimento.values())

# Inicializa o vetorizador para transformar texto em representação numérica (TF-IDF)
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(perguntas_treino)

# --- ROTAS DE AUTENTICAÇÃO ---

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/registrar', methods=['POST'])
def registrar():
    nome = request.form.get('nome_cadastro')
    email = request.form.get('email_cadastro')
    senha = request.form.get('senha_cadastro')
    if Usuario.query.filter_by(email=email).first():
        flash("Este e-mail já está cadastrado!")
        return redirect(url_for('login_page'))
    novo_usuario = Usuario(nome=nome, email=email, senha=senha)
    try:
        db.session.add(novo_usuario)
        db.session.commit()
        flash("Conta criada com sucesso!")
    except Exception as e:
        db.session.rollback()
        flash("Erro ao criar conta.")
    return redirect(url_for('login_page'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('nome')
    senha = request.form.get('senha')
    if email == "admin@cyberchase.com.br" and senha == "root":
        session['usuario_logado'] = "Administrador"
        return redirect(url_for('listar_cursos'))
    usuario = Usuario.query.filter_by(email=email).first()
    if usuario and usuario.senha == senha:
        session['usuario_logado'] = usuario.nome
        return redirect(url_for('index'))
    flash("E-mail ou senha incorretos!")
    return redirect(url_for('login_page'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

# --- ROTAS DO SISTEMA ---

@app.route('/home')
def index():
    if 'usuario_logado' not in session:
        return redirect(url_for('login_page'))
    return render_template('index.html')

# ROTA DO CHATBOT COM MACHINE LEARNING
@app.route('/ask', methods=['POST'])
def ask_bot():
    if 'usuario_logado' not in session:
        return jsonify({"response": "Por favor, faça login primeiro."}), 401

    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"response": "Diga algo para eu te ajudar!"})

    # Transforma o input do usuário e calcula similaridade de cosseno
    query_vec = vectorizer.transform([user_message])
    similaridade = cosine_similarity(query_vec, tfidf_matrix)
    
    indice_melhor = np.argmax(similaridade)
    score_confianca = similaridade[0][indice_melhor]

    # Define um limite de confiança (0.3 é um bom começo)
    if score_confianca > 0.3:
        resposta = respostas_treino[indice_melhor]
    else:
        resposta = "Ainda estou aprendendo sobre isso. Pode tentar perguntar sobre nossos cursos ou sobre a Cyber Chase?"

    return jsonify({"response": resposta})

@app.route('/courses')
def page_courses():
    if 'usuario_logado' not in session:
        return redirect(url_for('login_page'))
    cursos = Curso.query.all()
    return render_template('courses.html', cursos=cursos)

@app.route('/course/<int:id>')
def visualizar_curso(id):
    if 'usuario_logado' not in session:
        return redirect(url_for('login_page'))
    curso = db.session.get(Curso, id)
    if not curso:
        flash("Curso não encontrado.")
        return redirect(url_for('page_courses'))
    return render_template('course-details.html', curso=curso)

@app.route('/about')
def page_about():
    if 'usuario_logado' not in session:
        return redirect(url_for('login_page'))
    return render_template('about.html')

@app.route('/contact')
def page_contact():
    if 'usuario_logado' not in session:
        return redirect(url_for('login_page'))
    return render_template('contact.html')

# --- CRUD ADMIN ---

@app.route('/admin/cursos')
def listar_cursos():
    if 'usuario_logado' not in session:
        return redirect(url_for('login_page'))
    cursos = Curso.query.all()
    return render_template('admin-courses.html', cursos=cursos)

@app.route('/admin/cursos/novo', methods=['POST'])
def criar_curso():
    if 'usuario_logado' not in session: return redirect(url_for('login_page'))
    novo = Curso(
        titulo=request.form.get('titulo'),
        descricao=request.form.get('descricao'),
        conteudo=request.form.get('conteudo'),
        link=request.form.get('link') or None
    )
    db.session.add(novo)
    db.session.commit()
    return redirect(url_for('listar_cursos'))

@app.route('/admin/cursos/editar/<int:id>', methods=['POST'])
def editar_curso(id):
    if 'usuario_logado' not in session: return redirect(url_for('login_page'))
    curso = db.session.get(Curso, id)
    if curso:
        curso.titulo = request.form.get('titulo')
        curso.descricao = request.form.get('descricao')
        curso.conteudo = request.form.get('conteudo')
        curso.link = request.form.get('link')
        db.session.commit()
    return redirect(url_for('listar_cursos'))

@app.route('/admin/cursos/deletar/<int:id>')
def deletar_curso(id):
    if 'usuario_logado' not in session: return redirect(url_for('login_page'))
    curso = db.session.get(Curso, id)
    if curso:
        db.session.delete(curso)
        db.session.commit()
    return redirect(url_for('listar_cursos'))

if __name__ == '__main__':
    app.run(debug=True)