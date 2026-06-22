from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime

#configuracao inicial
base_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=base_dir, static_folder=base_dir, static_url_path='')
app.secret_key = "cyber_chase_secret_key"

#banco de dados em mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@127.0.0.1:3306/cyber_chase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#models bd
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
    descricao = db.Column(db.Text, nullable=False)
    conteudo = db.Column(db.Text, nullable=True)
    link = db.Column(db.String(900), nullable=True)
    pergunta_teste = db.Column(db.Text, nullable=True)   
    resposta_correta = db.Column(db.Text, nullable=True) 

with app.app_context():
    db.create_all()

# --- INTELIGÊNCIA DO CHATBOT ---
conhecimento = {
    "O que é a Cyber Chase?": "A Cyber Chase é uma organização focada em educação cibernética gratuita para ajudar você a construir seu escudo digital.",
    "Quais os benefícios da plataforma?": "Além de aprender a se proteger, você turbina seu currículo com nossos certificados de conclusão!",
    "Como funcionam os cursos?": "Nossos cursos são divididos em trilhas de aprendizado com testes para validar seu conhecimento.",
    "Quem é o Cybot?": "Eu sou o Cybot, seu assistente virtual e guardião da Cyber Chase!",
    "Como posso me proteger de ataques?": "Recomendamos o uso de senhas fortes, autenticação em dois fatores (2FA) e muita atenção a links suspeitos.",
    "A plataforma emite certificado?": "Sim! Ao concluir nossos cursos e passar nos testes, você recebe um certificado da Cyber Chase.",
    "Como entrar em contato?": "Você pode acessar nossa página de Contato no menu superior para falar com o time.",
    "Cai em um golpe, o que eu faço?": "Troque todas as senhas imediatamente, se necessário, registre um boletim de ocorrência e fique atento a atividades suspeitas em suas contas.",
    "O que é Phishing?": "Phishing é um tipo de ataque onde o criminoso tenta enganar a vítima para obter informações pessoais, como senhas e dados bancários, geralmente por meio de e-mails ou mensagens falsas.",
    "O que é Ransomware?": "Ransomware é um tipo de malware que sequestra os arquivos da vítima, criptografando-os e exigindo um resgate para liberá-los.",
    "O que é Engenharia Social?": "Engenharia Social é uma técnica de manipulação psicológica usada por criminosos para enganar pessoas e obter informações confidenciais ou acesso a sistemas.",
    "Como criar uma senha forte?": "Use uma combinação de letras maiúsculas, minúsculas, números e símbolos. Evite usar informações pessoais e palavras comuns.",
    "O que é autenticação em dois fatores (2FA)?": "2FA é um método de segurança que exige duas formas de identificação para acessar uma conta, geralmente uma senha e um código enviado para o celular.",
    "O que é um firewall?": "Um firewall é uma barreira de segurança que monitora e controla o tráfego de rede, bloqueando acessos não autorizados.",
    "O que é um antivírus?": "Um antivírus é um software projetado para detectar, prevenir e remover malware do seu computador.",
    "O que é um ataque DDoS?": "DDoS (Distributed Denial of Service) é um ataque onde múltiplos sistemas comprometidos são usados para sobrecarregar um alvo, como um site, tornando-o indisponível.",
    "O que é um VPN?": "VPN (Virtual Private Network) é uma tecnologia que cria uma conexão segura e criptografada entre seu dispositivo e a internet, protegendo sua privacidade online.",
    "O que é um ataque de força bruta?": "Um ataque de força bruta é uma tentativa de adivinhar senhas ou chaves de criptografia tentando todas as combinações possíveis até encontrar a correta.",
    "O que é um ataque de engenharia social?": "Um ataque de engenharia social é uma técnica onde o atacante manipula pessoas para obter informações confidenciais ou acesso a sistemas, muitas vezes se passando por alguém confiável."
}

perguntas_treino = list(conhecimento.keys())
respostas_treino = list(conhecimento.values())
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


@app.route('/home')
def index():
    if 'usuario_logado' not in session:
        return redirect(url_for('login_page'))
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_bot():
    if 'usuario_logado' not in session:
        return jsonify({"response": "Por favor, faça login primeiro."}), 401
    data = request.json
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"response": "Diga algo para eu te ajudar!"})
    query_vec = vectorizer.transform([user_message])
    similaridade = cosine_similarity(query_vec, tfidf_matrix)
    indice_melhor = np.argmax(similaridade)
    score_confianca = similaridade[0][indice_melhor]
    resposta = respostas_treino[indice_melhor] if score_confianca > 0.3 else "Ainda estou aprendendo sobre isso."
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
    
    nome_usuario = session.get('usuario_logado')
    data_atual = datetime.now().strftime('%d/%m/%Y')
    
    return render_template('course-details.html', curso=curso, nome_usuario=nome_usuario, data_hoje=data_atual)

# rota de validação da resposta do usuário para o teste do curso, usando IA para comparar com a resposta correta do banco
@app.route('/validar_teste/<int:id>', methods=['POST'])
def validar_teste(id):
    curso = db.session.get(Curso, id)
    dados = request.json
    resposta_usuario = dados.get("resposta", "").strip()

    if not curso or not curso.resposta_correta:
        return jsonify({"status": "sucesso"}) # se não houver resposta correta cadastrada, aprova automaticamente

    #inteligência artificial para comparar a resposta do usuário com a resposta cadastrada no banco de dados, usando TF-IDF e similaridade de cosseno
    textos = [curso.resposta_correta, resposta_usuario]
    vec_ia = TfidfVectorizer()
    try:
        tfidf = vec_ia.fit_transform(textos)
        similaridade = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    except:
        similaridade = 0

    #se a similaridade for maior que 35%, aprova
    if similaridade > 0.35:
        return jsonify({"status": "sucesso"})
    else:
        return jsonify({"status": "erro", "message": "Sua resposta não foi profunda o suficiente ou está incorreta. Tente explicar melhor."})

@app.route('/about')
def page_about():
    if 'usuario_logado' not in session: return redirect(url_for('login_page'))
    return render_template('about.html')

@app.route('/contact')
def page_contact():
    if 'usuario_logado' not in session: return redirect(url_for('login_page'))
    return render_template('contact.html')

# --- CRUD ADMIN ---

@app.route('/admin/cursos')
def listar_cursos():
    if 'usuario_logado' not in session: return redirect(url_for('login_page'))
    cursos = Curso.query.all()
    return render_template('admin-courses.html', cursos=cursos)

@app.route('/admin/cursos/novo', methods=['POST'])
def criar_curso():
    if 'usuario_logado' not in session: return redirect(url_for('login_page'))
    novo = Curso(
        titulo=request.form.get('titulo'),
        descricao=request.form.get('descricao'),
        conteudo=request.form.get('conteudo'),
        link=request.form.get('link') or None,
        pergunta_teste=request.form.get('pergunta_teste'), 
        resposta_correta=request.form.get('resposta_correta') 
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
        curso.pergunta_teste = request.form.get('pergunta_teste') 
        curso.resposta_correta = request.form.get('resposta_correta') 
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