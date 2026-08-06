campo_saldo = document.getElementById('saldo-saldo');
if (campo_saldo) {
    campo_saldo.addEventListener('input', function(e) {
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

campo_ano = document.getElementById('ano-saldo');
if (campo_ano) {
    campo_ano.addEventListener('input', function(e) {
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

const modalEditSaldo = document.getElementById('modalEditSaldo');
modalEditSaldo.addEventListener('show.bs.modal', function(e) {
    const botao = e.relatedTarget;

    if (botao) {
        const input_id = document.getElementById('id-edit-saldo');
        const input_banco = document.getElementById('banco-edit-saldo');
        const input_saldo = document.getElementById('saldo-edit-saldo');
        const titulo_modal = document.getElementById('modalEditSaldoLabel');

        titulo_modal.innerHTML = `Editar ${botao.dataset.tipoSaldo}`;
        input_id.value = botao.dataset.id;
        input_banco.value = botao.dataset.banco;
        input_banco.style.height = ''; 
        input_saldo.value = botao.dataset.saldo;

        const eventoInput = new Event('input');
        input_saldo.dispatchEvent(eventoInput);
    }
});

campo_editar_banco_saldo = document.getElementById('banco-edit-saldo');
if (campo_editar_banco_saldo) {
    campo_editar_banco_saldo.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
        }
    });
}

campo_editar_valor_saldo = document.getElementById('saldo-edit-saldo');
if (campo_editar_valor_saldo) {
    campo_editar_valor_saldo.addEventListener('input', function(e) {
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