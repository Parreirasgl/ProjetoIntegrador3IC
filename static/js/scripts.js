let zoomLevel = 1;

// Função para alternar contraste
function toggleContrast() {
    const body = document.body;
    body.classList.toggle('high-contrast'); // Alterna a classe de contraste alto
    console.log('toggleContrast foi chamado'); // Para depuração
}

// Função para aumentar o zoom
function zoomIn() {
    let currentZoom = parseFloat(getComputedStyle(document.body).fontSize);
    document.body.style.fontSize = (currentZoom * 1.1) + 'px'; // Aumenta o tamanho da fonte em 10%
    console.log('zoomIn foi chamado'); // Para depuração
}

// Função para reduzir o zoom
function zoomOut() {
    let currentZoom = parseFloat(getComputedStyle(document.body).fontSize);
    document.body.style.fontSize = (currentZoom / 1.1) + 'px'; // Reduz o tamanho da fonte em 10%
    console.log('zoomOut foi chamado'); // Para depuração
}

document.addEventListener("DOMContentLoaded", function() {
    // Adicionar o listener para o formulário de contato
    document.getElementById('contactForm').addEventListener('submit', function(event) {
        event.preventDefault();

        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const message = document.getElementById('message').value;

        fetch('https://exemplo.com/api/enviar-contato', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name, email, message }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao enviar a mensagem.');
            }
            return response.json();
        })
        .then(data => {
            document.getElementById('responseMessage').innerHTML = '<div class="alert alert-success">Mensagem enviada com sucesso!</div>';
            document.getElementById('contactForm').reset();
        })
        .catch(error => {
            document.getElementById('responseMessage').innerHTML = '<div class="alert alert-danger">Erro: ' + error.message + '</div>';
        });
    });

    // Adicionar o listener para o formulário de login
    document.getElementById('loginForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Evita o envio padrão do formulário

        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        // Simulando o envio para um servidor (substitua a URL pelo endpoint real)
        fetch('https://exemplo.com/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao realizar o login.');
            }
            return response.json();
        })
        .then(data => {
            document.getElementById('loginResponseMessage').innerHTML = '<div class="alert alert-success">Login realizado com sucesso!</div>';
            // Aqui você pode redirecionar para outra página ou armazenar um token de autenticação, etc.
        })
        .catch(error => {
            document.getElementById('loginResponseMessage').innerHTML = '<div class="alert alert-danger">Erro: ' + error.message + '</div>';
        });
    });
});