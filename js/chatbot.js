const chatBody = document.getElementById('chatbot-body');
const userInput = document.querySelector('.user-input');

// Função principal para enviar mensagem
async function sendMessage() {
    const message = userInput.value.trim();
    if (message === "") return;

    // 1. Mostrar mensagem do usuário
    addBubble(message, 'user-bubble');
    userInput.value = "";

    try {
        // 2. Enviar para o Flask (main.py)
        const response = await fetch('/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        // 3. Mostrar resposta do Cybot
        addBubble(data.response, 'bot-bubble');

        // 4. Se a resposta sugerir opções, podemos criar botões (opcional)
        if (message.toLowerCase().includes("ajuda") || message.toLowerCase().includes("oi")) {
            showOptions();
        }

    } catch (error) {
        addBubble("Erro de conexão com o servidor.", 'bot-bubble');
    }
}

// Função para adicionar os balões na tela
function addBubble(text, type) {
    const bubble = document.createElement('div');
    bubble.className = `bubble ${type}`;
    bubble.innerText = text;
    chatBody.appendChild(bubble);
    chatBody.scrollTop = chatBody.scrollHeight;
}

// Função para mostrar as opções que você tinha no código antigo
function showOptions() {
    const optionsContainer = document.createElement('div');
    optionsContainer.className = 'options-container';
    optionsContainer.style.display = 'flex';
    optionsContainer.style.gap = '5px';
    optionsContainer.style.padding = '10px';

    const options = [
        { label: "O que é a Cyber Chase?", value: "O que é a Cyber Chase?" },
        { label: "Benefícios", value: "Quais os benefícios?" }
    ];

    options.forEach(opt => {
        const btn = document.createElement('button');
        btn.innerText = opt.label;
        btn.className = 'option-btn'; // Adicione estilo no seu CSS
        btn.onclick = () => {
            userInput.value = opt.value;
            sendMessage();
            optionsContainer.remove();
        };
        optionsContainer.appendChild(btn);
    });

    chatBody.appendChild(optionsContainer);
    chatBody.scrollTop = chatBody.scrollHeight;
}

// Evento de tecla Enter
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});