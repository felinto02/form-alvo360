// Função para carregar e pré-visualizar a foto selecionada
function setupImagePreview(inputId, imageId) {
    document.getElementById(inputId).addEventListener('change', function(event) {
        const pictureInput = event.target;
        const pictureImage = document.getElementById(imageId);

        if (pictureInput.files && pictureInput.files[0]) {
            const reader = new FileReader();
            reader.onload = function(e) {
                pictureImage.textContent = ''; // Remove o texto "Selecione a imagem"
                const img = document.createElement('img');
                img.src = e.target.result;
                img.alt = 'Foto de pré-visualização';
                img.style.maxWidth = '100%';  // Define um tamanho máximo para a imagem
                img.style.height = 'auto';
                pictureImage.appendChild(img); // Adiciona a imagem pré-visualizada
            };
            reader.readAsDataURL(pictureInput.files[0]);
        } else {
            pictureImage.textContent = 'Selecione a imagem'; // Caso nenhum arquivo seja selecionado
        }
    });
}

// Chamar a função para cada input de imagem
setupImagePreview('picture-input-1', 'picture-image-1');
setupImagePreview('picture-input-2', 'picture-image-2');
setupImagePreview('picture-input-3', 'picture-image-3');



// Função para formatar o campo de CPF com pontos e traço (formato brasileiro)
function formatCPF(input) {
    let value = input.value.replace(/\D/g, ''); // Remove qualquer caractere que não seja número
    value = value.replace(/(\d{3})(\d)/, '$1.$2'); // Adiciona o primeiro ponto
    value = value.replace(/(\d{3})(\d)/, '$1.$2'); // Adiciona o segundo ponto
    value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2'); // Adiciona o traço
    input.value = value.substring(0, 14); // Limita o valor em 14 caracteres
}

// Função para formatar o campo de telefone com parênteses e traço
function formatPhone(input) {
    let value = input.value.replace(/\D/g, ''); // Remove qualquer caractere que não seja número
    value = value.replace(/(\d{2})(\d)/, '($1) $2'); // Adiciona o DDD entre parênteses
    value = value.replace(/(\d{5})(\d)/, '$1-$2'); // Adiciona o traço após os primeiros 5 dígitos
    input.value = value.substring(0, 15); // Limita o valor em 15 caracteres
}

// Função para capitalizar a primeira letra de cada palavra do nome, exceto preposições
function capitalizeName(input) {
    let words = input.value.toLowerCase().split(' '); // Divide o nome em palavras
    for (let i = 0; i < words.length; i++) {
        if (words[i] !== 'de' && words[i] !== 'da') {
            words[i] = words[i].charAt(0).toUpperCase() + words[i].slice(1); // Capitaliza a primeira letra
        }
    }
    input.value = words.join(' '); // Junta as palavras de volta
}

// Função para limpar todos os campos do formulário e esconder imagens pré-visualizadas
function limparCampos() {
    const form = document.querySelector('form');
    form.reset(); // Reseta todos os campos do formulário

    // Limpa as imagens pré-visualizadas
    const imgElements = document.querySelectorAll('img'); // Seleciona todas as imagens
    imgElements.forEach(img => {
        img.src = ''; // Limpa a fonte da imagem
        img.style.display = 'none'; // Oculta a imagem
    });
}

// Evento disparado quando o DOM estiver totalmente carregado
document.addEventListener("DOMContentLoaded", function() {
    const nomeCompletoInput = document.getElementById('nome'); // Campo de entrada de nome completo
    const suggestionsContainer = document.getElementById('suggestions-container'); // Contêiner de sugestões
    let debounceTimeout;

    // Função para mostrar as sugestões de nomes
    function mostrarSugestoes(sugestoes) {
        suggestionsContainer.innerHTML = ''; // Limpa sugestões anteriores
        if (sugestoes.length === 0) {
            suggestionsContainer.style.display = 'none'; // Esconde contêiner se não houver sugestões
            return;
        }
        suggestionsContainer.style.display = 'block'; // Exibe contêiner de sugestões

        // Adiciona cada sugestão ao contêiner
        sugestoes.forEach(sugestao => {
            const item = document.createElement('div');
            item.classList.add('suggestion-item');
            item.textContent = sugestao;
            item.addEventListener('click', function() {
                nomeCompletoInput.value = sugestao; // Preenche o campo de nome com a sugestão selecionada
                buscarDadosCliente(sugestao); // Faz a requisição para buscar os dados completos do cliente
                suggestionsContainer.style.display = 'none'; // Esconde o contêiner após a seleção
            });
            suggestionsContainer.appendChild(item);
        });
    }

    // Função para buscar sugestões no servidor via AJAX
    async function buscarSugestoes(valorEntrada) {
        try {
            const response = await fetch(`/suggest_names?query=${valorEntrada}`); // Faz a requisição ao servidor
            const sugestoes = await response.json(); // Converte a resposta em JSON
            mostrarSugestoes(sugestoes); // Exibe as sugestões
        } catch (error) {
            console.error('Erro ao buscar sugestões:', error); // Exibe erro no console
        }
    }

    // Evento de input no campo de nome completo para buscar sugestões
    nomeCompletoInput.addEventListener('input', function() {
        capitalizeName(this);
        clearTimeout(debounceTimeout);
        debounceTimeout = setTimeout(() => {
            const valor = nomeCompletoInput.value.trim(); // Remove espaços em branco
            if (valor === '') {
                suggestionsContainer.style.display = 'none'; // Esconde sugestões se o campo estiver vazio
            } else {
                buscarSugestoes(valor); // Busca sugestões
            }
        }, 300); // Debounce de 300ms para evitar requisições constantes
    });

    // Oculta o contêiner de sugestões ao clicar fora dele
    document.addEventListener('click', function(event) {
        if (!suggestionsContainer.contains(event.target) && event.target !== nomeCompletoInput) {
            suggestionsContainer.style.display = 'none'; // Esconde o contêiner de sugestões
        }
    });
});

// Função para limpar campos ao clicar no botão 'Limpar'
document.getElementById('btnLimpar').addEventListener('click', function() {
    limparCampos(); // Limpa o formulário e as imagens

    // Adiciona animação ao formulário
    const formulario = document.getElementById('meuFormulario');
    formulario.classList.add('piscando');

    // Remove a animação após a execução
    setTimeout(function() {
        formulario.classList.remove('piscando');
    }, 80); // Duração da animação
});

// Função para buscar dados completos do cliente ao clicar em uma sugestão
async function buscarDadosCliente(nomeSelecionado) {
    try {
        const response = await fetch(`/buscar_dados_cliente?nome=${nomeSelecionado}`);
        const dados = await response.json();



        if (dados.error) {
            console.error('Cliente não encontrado:', dados.error);
            alert('Cliente não encontrado.');
            return;
        }

        // Preencher formulário com os dados recebidos
        preencherFormulario(dados);
    } catch (error) {
        console.error('Erro ao buscar dados do cliente:', error);
    }
}

function preencherFormulario(cliente) {
    // Preenche outros campos aqui, como nome, cpf, telefone, etc.

    // Preencher as fotos em base64, se disponíveis
    if (cliente.fotos && cliente.fotos.foto1) {
        document.getElementById('picture-image-1').innerText = '';  // Limpa o texto "Selecione a imagem"
        document.getElementById('preview_foto').src = `data:image/jpeg;base64,${cliente.fotos.foto1}`;
        document.getElementById('preview_foto').style.display = 'block';  // Exibe a imagem
    }
    if (cliente.fotos && cliente.fotos.foto2) {
        document.getElementById('picture-image-2').innerText = '';
        const img2 = document.createElement('img');
        img2.src = `data:image/jpeg;base64,${cliente.fotos.foto2}`;
        img2.style.maxWidth = '100%';
        img2.style.height = 'auto';
        document.getElementById('picture-image-2').appendChild(img2);
    }
    if (cliente.fotos && cliente.fotos.foto_casa) {
        document.getElementById('picture-image-3').innerText = '';
        const img3 = document.createElement('img');
        img3.src = `data:image/jpeg;base64,${cliente.fotos.foto_casa}`;
        img3.style.maxWidth = '100%';
        img3.style.height = 'auto';
        document.getElementById('picture-image-3').appendChild(img3);
    }

    // Preenchendo os outros campos
    document.getElementById('cliente_id').value = cliente.cliente.cliente_id || '';
    document.getElementById('nome').value = cliente.cliente.nome || '';
    document.getElementById('nome_mae').value = cliente.cliente.nome_mae || '';
    document.getElementById('nome_pai').value = cliente.cliente.nome_pai || '';

    // Convertendo a data_nasc de d/m/yyyy para YYYY-MM-DD
    if (cliente.cliente.data_nasc) {
        const partesData = cliente.cliente.data_nasc.split('/');
        if (partesData.length === 3 && document.getElementById('data_nasc')) {
            const dataNascFormatada = `${partesData[2]}-${partesData[1]}-${partesData[0]}`; // YYYY-MM-DD
            
            // Adicionando os console.log para verificar as datas
            console.log('Data de nascimento original:', cliente.cliente.data_nasc);
            console.log('Data de nascimento formatada:', dataNascFormatada);
            
            document.getElementById('data_nasc').value = dataNascFormatada;  // Atribuindo o valor formatado
        }
    }


    document.getElementById('nat').value = cliente.cliente.nat || '';
    document.getElementById('nat_uf').value = cliente.cliente.nat_uf || '';
    document.getElementById('cpf').value = cliente.cliente.cpf || '';
    document.getElementById('rg').value = cliente.cliente.rg || '';
    document.getElementById('telefone').value = cliente.cliente.telefone || '';
    document.getElementById('telefone_secundario').value = cliente.cliente.telefone_secundario || '';
    document.getElementById('observacao').value = cliente.cliente.observacao || '';

    // Preenchendo os dados do endereço
    if (cliente.endereco) {
        document.getElementById('logradouro').value = cliente.endereco.logradouro || '';
        document.getElementById('numero').value = cliente.endereco.numero || '';
        document.getElementById('complemento').value = cliente.endereco.complemento || '';
        document.getElementById('bairro').value = cliente.endereco.bairro || '';
        document.getElementById('cidade').value = cliente.endereco.cidade || '';
        document.getElementById('uf_endereco').value = cliente.endereco.uf || '';
        document.getElementById('obs_endereco').value = cliente.endereco.obs_endereco || '';
        document.getElementById('link_endereco').value = cliente.endereco.link_endereco || '';
    }

    // Preenchendo informações adicionais
    if (cliente.informacoes) {
        document.getElementById('info_adicionais').value = cliente.informacoes.info_adicionais || '';
        document.getElementById('nome_operacao').value = cliente.informacoes.nome_operacao || '';
    }
}


document.getElementById('gerarQRCode').addEventListener('click', function() {
    // Obtém o ID do cliente
    const clienteId = document.getElementById('cliente_id').value;

    // Verifica se o cliente_id está preenchido
    if (!clienteId) {
        alert("Por favor, preencha o campo de ID do cliente para gerar o QR Code.");
        return;
    }

    // Define a URL para gerar o PDF com QR Code
    const url = `/gerar_qrcode_pdf/${clienteId}`;

    // Redireciona o usuário para a URL gerada para download do PDF
    window.location.href = url;
});
