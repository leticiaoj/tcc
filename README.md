
**VÍDEO DE APRESENTAÇÃO DO PROJETO:** [Assista à apresentação do Cyber Chase no YouTube](https://youtu.be/3YQVgy0ku5M?is=Ql3MfpGz2REdRvo1)

# CYBER CHASE

## Plataforma Web Educacional para Mitigação de Ataques Cibernéticos através da Conscientização Digital

## 1. Sobre o projeto

- Projeto desenvolvido como Trabalho de Conclusão de Curso (TCC) do Bacharelado em Sistemas de Informação da Universidade Paulista (UNIP).
- Plataforma web educacional voltada à conscientização e à segurança digital.
- Objetivo principal: contribuir para a mitigação de ataques cibernéticos por meio da educação e da aprendizagem interativa.
- Aborda ameaças que exploram vulnerabilidades humanas e tecnológicas, como phishing, engenharia social e fraudes digitais.

## 2. Objetivos

- Promover a conscientização sobre segurança cibernética.
- Disponibilizar conteúdos educacionais sobre ameaças digitais.
- Oferecer ferramentas interativas para apoiar o aprendizado.
- Utilizar Inteligência Artificial e Machine Learning no processamento e na avaliação de respostas textuais.
- Incentivar práticas mais seguras no ambiente digital.

## 3. Funcionalidades

- **Cadastro e autenticação**
  - Criação de contas e login.
  - Gerenciamento de sessões dos usuários.
  - Controle de acesso às páginas internas.

- **Catálogo de cursos**
  - Visualização dos cursos disponíveis.
  - Acesso aos conteúdos educacionais.
  - Navegação entre as trilhas de aprendizagem.

- **Cursos interativos**
  - Apresentação de conteúdos sobre segurança digital.
  - Atividades e perguntas avaliativas.
  - Validação automatizada das respostas.

- **Cybot — Assistente virtual**
  - Chatbot educacional para esclarecimento de dúvidas.
  - Utilização de uma base de conhecimento predefinida.
  - Identificação de perguntas por similaridade textual.

- **Avaliação automatizada**
  - Comparação entre as respostas dos usuários e as respostas de referência.
  - Aplicação de técnicas de Processamento de Linguagem Natural.
  - Critério de aprovação baseado em similaridade textual.

- **Certificados**
  - Emissão após a aprovação na avaliação do curso.
  - Disponibilização dos certificados ao usuário.

- **Perfil do usuário**
  - Visualização dos cursos em andamento.
  - Acompanhamento dos cursos concluídos.
  - Acesso aos certificados emitidos.

- **Painel administrativo**
  - Gerenciamento de cursos e conteúdos.
  - Administração de links e perguntas avaliativas.
  - Operações CRUD: Create, Read, Update e Delete.

## 4. Conteúdos educacionais

A plataforma contempla seis trilhas de aprendizagem:

1. Ataques Cibernéticos.
2. Engenharia Social.
3. Phishing.
4. Vírus.
5. Segurança em Dispositivos Móveis.
6. Forense Digital e Respostas a Incidentes.

## 5. Inteligência Artificial e Machine Learning

O projeto utiliza técnicas de Processamento de Linguagem Natural (PLN) e Machine Learning em duas funcionalidades principais.

### 5.1. Cybot — Chatbot educacional

- Utiliza uma base de conhecimento composta por perguntas e respostas predefinidas.
- Aplica vetorização de textos por meio de TF-IDF.
- Calcula a similaridade textual utilizando a similaridade do cosseno.
- Identifica a pergunta cadastrada mais compatível com a entrada do usuário.
- Utiliza o limiar de similaridade de 0,3 para determinar se existe correspondência suficiente.

### 5.2. Validação das respostas

- Compara as respostas enviadas pelos usuários com as respostas de referência cadastradas.
- Utiliza técnicas de similaridade textual para auxiliar na avaliação.
- Aplica um limiar de similaridade de 35%.
- Permite a aprovação e a emissão do certificado quando o critério estabelecido é atendido.

## 6. Tecnologias utilizadas

- **HTML5**
  - Estruturação das páginas e dos conteúdos.

- **CSS3**
  - Estilização e organização visual das interfaces.

- **JavaScript**
  - Implementação de interações e funcionalidades no front-end.

- **Python**
  - Desenvolvimento do back-end e processamento textual.

- **Flask**
  - Gerenciamento de rotas HTTP, sessões, autenticação e regras de negócio.

- **MySQL**
  - Banco de dados relacional para armazenamento das informações.

- **SQLAlchemy**
  - Mapeamento objeto-relacional (ORM) e interação com o banco de dados.

- **Scikit-learn**
  - Implementação de técnicas de Machine Learning e vetorização TF-IDF.

- **TF-IDF**
  - Representação numérica dos textos para comparação de conteúdo.

- **Similaridade do cosseno**
  - Cálculo da proximidade entre textos.

- **Git e GitHub**
  - Versionamento e hospedagem do código-fonte.

## 7. Arquitetura da aplicação

A aplicação foi desenvolvida como uma solução web monolítica, organizada em quatro camadas:

- **Camada de apresentação**
  - HTML, CSS, JavaScript e templates Flask.
  - Responsável pela interface, navegação, formulários e exibição de respostas.

- **Camada de aplicação**
  - Python e Flask.
  - Responsável pelas rotas HTTP, autenticação, sessões e regras de negócio.

- **Camada de inteligência artificial**
  - Scikit-learn, TF-IDF e similaridade do cosseno.
  - Responsável pelo funcionamento do Cybot e pela validação textual das respostas.

- **Camada de persistência**
  - MySQL e SQLAlchemy.
  - Responsável pelo armazenamento e gerenciamento dos dados.

## 8. Metodologia de desenvolvimento

- Metodologia baseada em uma adaptação do Scrum.
- Desenvolvimento organizado em 10 sprints.
- Utilização de prototipação incremental.
- Entregas progressivas e validação contínua.

### Etapas de desenvolvimento

1. Estruturação inicial das páginas em HTML.
2. Estilização das interfaces com CSS.
3. Desenvolvimento do back-end com Python e Flask.
4. Integração com MySQL e SQLAlchemy.
5. Implementação da autenticação e do gerenciamento de sessões.
6. Desenvolvimento do CRUD administrativo.
7. Implementação do chatbot Cybot.
8. Exibição dinâmica dos cursos.
9. Implementação da validação textual com PLN.
10. Realização de testes funcionais e refinamentos.

## 9. Testes e validação

Foram realizados testes funcionais para verificar:

- Cadastro, login e controle de sessão.
- Operações administrativas de criação, consulta, atualização e exclusão de cursos.
- Integração e funcionamento do chatbot Cybot.
- Processamento e comparação de textos.
- Validação das respostas dos cursos.
- Emissão de certificados após a aprovação.

Os resultados foram analisados qualitativamente, considerando o funcionamento dos recursos implementados dentro do escopo proposto.

## 10. Melhorias futuras

- Ampliação dos relacionamentos entre as tabelas do banco de dados.
- Implementação de novas integrações.
- Expansão dos recursos de gamificação.
- Evolução dos mecanismos de interação e aprendizagem.

## 11. Autoras

- **Julia Cristina Silva de Souza**
- **Leticia Oliveira de Jesus**

**Instituição:** Universidade Paulista (UNIP)
**Curso:** Bacharelado em Sistemas de Informação
**Tipo de trabalho:** Trabalho de Conclusão de Curso (TCC)
**Local:** São Paulo
**Ano:** 2026

## 12. Considerações finais

- O Cyber Chase reúne recursos de desenvolvimento web, banco de dados e Inteligência Artificial.
- A plataforma utiliza técnicas de Machine Learning e Processamento de Linguagem Natural para apoiar a aprendizagem.
- O projeto busca contribuir para a conscientização sobre ameaças digitais e incentivar hábitos mais seguros no uso da tecnologia.
