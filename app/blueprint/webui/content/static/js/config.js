const meuModal = document.getElementById('modalEditBanco');
meuModal.addEventListener('show.bs.modal', function(e) {
    const botao = e.relatedTarget;

    if (botao) {
        const input_id = document.getElementById('id-edit');
        const input_nome = document.getElementById('nome-edit');
        
        input_id.value = botao.dataset.bancoId;
        input_nome.value = botao.dataset.bancoNome;
    }
});