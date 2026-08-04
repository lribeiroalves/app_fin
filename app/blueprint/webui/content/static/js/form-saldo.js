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