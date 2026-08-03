btn_nova_entrada = document.getElementById('btn-nova-entrada');

function abrirModalEntrada() {
    const modalEntrada = bootstrap.Modal.getOrCreateInstance(document.getElementById('modalEntrada'));
    modalEntrada.show();
}