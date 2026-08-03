desc_entrada = document.getElementById('desc-entrada');
if (desc_entrada) {
    desc_entrada.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
        }
    });
}

valor_entrada = document.getElementById('valor-entrada');
if (valor_entrada) {
    valor_entrada.addEventListener('input', function(e) {
        let valorAtual = this.value;
    
        valorAtual = valorAtual.replace(/[^0-9.,]/g, '');
    
        valorAtual = valorAtual.replace(/\./g, ',');
    
        const partes = valorAtual.split(',');
    
        if (partes[0].length === 0) {
            this.value = '';
            return;
        }
    
        if (partes.length > 2) {
                valorAtual = partes[0] + ',' + partes.slice(1).join('').replace(/,/g, '');
            }
        
        const partesFinais = valorAtual.split(',');
        if (partesFinais.length === 2) {
            let decimais = partesFinais[1].substring(0, 2);
            valorAtual = partesFinais[0] + ',' + decimais;
        }
    
        this.value = valorAtual;
    });
}

ano_entrada = document.getElementById('ano-entrada');
if (ano_entrada) {
    ano_entrada.addEventListener('input', function(e) {
        let valorAtual = this.value;
    
        valorAtual = valorAtual.replace(/[^0-9]/g, '');
    
        if (valorAtual.length > 4) {
            valorAtual = valorAtual.substring(0, 4);
        }
    
        this.value = valorAtual;
    
        if (this.value.length === 0) {
            this.setCustomValidity("O campo precisa ser preenchido.")
        } else if (this.value.length > 0 && this.value.length < 4) {
            this.setCustomValidity("O ano deve conter exatamente 4 dígitos.");
        } else if (this.value.length === 4 && parseInt(this.value) < 2026) {
            this.setCustomValidity("O ano não pode ser menor que 2026.");
        } else {
            this.setCustomValidity(""); 
        }
    });
}


function abrirConfirmacao() {
    const form = document.getElementById('form-entrada');

    // Conferir campos
    if (!form.reportValidity()) {
        return;
    }

    // Coletar valores
    const selUser = document.getElementById('user-entrada');
    document.getElementById('conf-user').textContent = selUser.options[selUser.selectedIndex].text;

    document.getElementById('conf-ano').textContent = document.getElementById('ano-entrada').value;

    const selMes = document.getElementById('mes-entrada');
    document.getElementById('conf-mes').textContent = selMes.options[selMes.selectedIndex].text;

    document.getElementById('conf-valor').textContent = document.getElementById('valor-entrada').value;

    document.getElementById('conf-desc').textContent = document.getElementById('desc-entrada').value;

    // Alternar modais
    const modalTransacao = bootstrap.Modal.getOrCreateInstance(document.getElementById('modalTransacao'));
    modalTransacao.hide();
    
    const modalConfirmacao = bootstrap.Modal.getOrCreateInstance(document.getElementById('modalConfirmacao'));
    modalConfirmacao.show();
}

function voltarParaEdicao() {
    const modalConfirmacao = bootstrap.Modal.getOrCreateInstance(document.getElementById('modalConfirmacao'));
    modalConfirmacao.hide();

    const modalTransacao = bootstrap.Modal.getOrCreateInstance(document.getElementById('modalTransacao'));
    modalTransacao.show();
    
}

function enviarFormulario() {
    document.getElementById('form-entrada').submit();
}

const meuModal = document.getElementById('modalTransacao');
meuModal.addEventListener('show.bs.modal', function(e) {
    const botao = e.relatedTarget;

    const tipo = botao.getAttribute('data-tipo');

    const campo_tipo = meuModal.querySelector('#tipo');
    campo_tipo.value = tipo;

    const tituloModal = meuModal.querySelector('#modalTransacaoLabel');
    tituloModal.textContent = `Adicionar Nova ${tipo[0].toUpperCase() + tipo.slice(1)}`;
});