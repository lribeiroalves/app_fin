campo_desc_transacao = document.getElementById('desc-transacao');
if (campo_desc_transacao) {
    campo_desc_transacao.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
        }
    });
}

campo_valor_transacao = document.getElementById('valor-transacao');
if (campo_valor_transacao) {
    campo_valor_transacao.addEventListener('input', function(e) {
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

campo_ano_transacao = document.getElementById('ano-transacao');
if (campo_ano_transacao) {
    campo_ano_transacao.addEventListener('input', function(e) {
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


function abrirConfirmacao(form_name) {
    const form = document.getElementById(`form-${form_name}`);

    // Conferir campos
    if (!form.reportValidity()) {
        return;
    }

    // Coletar valores
    const selUser = document.getElementById(`user-${form_name}`);
    document.getElementById('conf-user').textContent = selUser.options[selUser.selectedIndex].text;

    document.getElementById('conf-ano').textContent = document.getElementById(`ano-${form_name}`).value;

    const selMes = document.getElementById(`mes-${form_name}`);
    document.getElementById('conf-mes').textContent = selMes.options[selMes.selectedIndex].text;

    conf_valor = document.getElementById('conf-valor');
    conf_desc = document.getElementById('conf-desc');
    conf_banco = document.getElementById('conf-banco');
    texto_valor = document.getElementById('conf-texto-valor');
    texto_desc = document.getElementById('conf-texto-desc');
    texto_banco = document.getElementById('conf-texto-banco');

    btn_voltar = document.getElementById('conf-voltar');
    btn_submeter = document.getElementById('conf-submeter');
    
    if (form_name === 'transacao') {
        conf_valor.textContent = document.getElementById('valor-transacao').value;
        texto_valor.innerHTML = 'Valor:'
        
        conf_desc.textContent = document.getElementById('desc-transacao').value;
        texto_desc.innerHTML = "Descrição:"

        conf_banco.textContent = "";
        texto_banco.innerHTML = "";

        const modalTransacao = bootstrap.Modal.getOrCreateInstance(document.getElementById('modalTransacao'));
        modalTransacao.hide();

        btn_voltar.dataset.formOrigem = "transacao";
        btn_submeter.dataset.formOrigem = "transacao";

    } else if (form_name === 'saldo') {
        conf_valor.textContent = document.getElementById('saldo-saldo').value;
        texto_valor.innerHTML = 'Saldo:'
        
        conf_desc.textContent = "";
        texto_desc.innerHTML = "";

        texto_banco.innerHTML = "Banco:";
        const selBanco = document.getElementById(`banco-${form_name}`);
        conf_banco.textContent = selBanco.options[selBanco.selectedIndex].text;

        const modalSaldo = bootstrap.Modal.getOrCreateInstance(document.getElementById('modalSaldo'));
        modalSaldo.hide();

        btn_voltar.dataset.formOrigem = "saldo";
        btn_submeter.dataset.formOrigem = "saldo";
    }

    // Alternar modais    
    const modalConfirmacao = bootstrap.Modal.getOrCreateInstance(document.getElementById('modalConfirmacao'));
    modalConfirmacao.show();
}

function voltarParaEdicao() {
    btn_voltar = document.getElementById('conf-voltar');

    const modalConfirmacao = bootstrap.Modal.getOrCreateInstance(document.getElementById('modalConfirmacao'));
    modalConfirmacao.hide();
    
    if (btn_voltar.dataset.formOrigem === 'transacao') {
        const modalTransacao = bootstrap.Modal.getOrCreateInstance(document.getElementById('modalTransacao'));
        modalTransacao.show();
    } else if (btn_voltar.dataset.formOrigem === 'saldo') {
        const modalTransacao = bootstrap.Modal.getOrCreateInstance(document.getElementById('modalSaldo'));
        modalTransacao.show();
    }
}

function enviarFormulario() {
    btn_submeter = document.getElementById('conf-submeter');

    if (btn_submeter.dataset.formOrigem === 'transacao') {
        document.getElementById('form-transacao').submit();
    } else if (btn_submeter.dataset.formOrigem === 'saldo') {
        document.getElementById('form-saldo').submit();
    }
}

const meuModal = document.getElementById('modalTransacao');
meuModal.addEventListener('show.bs.modal', function(e) {
    const botao = e.relatedTarget;

    if (botao) {
        const tipo = botao.getAttribute('data-tipo');
    
        const campo_tipo = meuModal.querySelector('#tipo');
        campo_tipo.value = tipo;
    
        const tituloModal = meuModal.querySelector('#modalTransacaoLabel');
        tituloModal.textContent = `Adicionar Nova ${tipo[0].toUpperCase() + tipo.slice(1)}`;
    }
});