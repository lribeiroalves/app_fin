import { graficoPatrimonio } from "./graficoPatrimonio.js";
import { graficoFluxo } from "./graficoFluxo.js";

var usuarioSelecionado1 = 0;
var usuarioSelecionado2 = 0;
var anoSelecionado1 = 0;
var anoSelecionado2 = 0;
var mesesSelecionados2 = {};
var mesesSelecionados1 = {};
var payload = {}

$("input[type=checkbox]").each(function() {
  mesesSelecionados1[this.id] = true;
  mesesSelecionados2[this.id] = true;
});

function exibirMensagem(mensagem, tipo="warning") {
    let $alerta = $(`
        <div class="alert alert-${tipo} alert-dismissible fade show text-center mx-5" role="alert">
            ${mensagem}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `);

    $('#flash-messages').append($alerta);

    setTimeout(function () {
        if ($.contains(document, $alerta[0])) {
            
            let bsAlert = new bootstrap.Alert($alerta[0]);
            bsAlert.close();
        }
    }, 3000);
}


$("#atualiza-grafico").on("click", function() {
    let selecaoLimpa = true;

    if ($(".tab-pane.active").attr("id") === "graf1") {
        $("input[type=checkbox]").each(function() {
            mesesSelecionados1[this.id] = $(this).prop("checked");
            if ($(this).prop("checked")) {
                selecaoLimpa = false;
            }
        });
        anoSelecionado1 = $("#selectAno").val();
        usuarioSelecionado1 = $("#selectUser").val();

        if (!anoSelecionado1) {
            exibirMensagem('Selecione um ano de referência!', 'danger');
            return;
        }

        if (!usuarioSelecionado1) {
            exibirMensagem('Selecione um usuário!', 'danger');
            return;
        }

        payload = {
            grafico: "graf1",
            meses: mesesSelecionados1,
            ano: anoSelecionado1,
            user: usuarioSelecionado1
        };

    } else if ($(".tab-pane.active").attr("id") === "graf2") {
        $("input[type=checkbox]").each(function() {
            mesesSelecionados2[this.id] = $(this).prop("checked");
            if ($(this).prop("checked")) {
                selecaoLimpa = false;
            }
        });
        anoSelecionado2 = $("#selectAno").val();
        usuarioSelecionado2 = $("#selectUser").val();

        if (!anoSelecionado2) {
            exibirMensagem('Selecione um ano de referência!', 'danger');
            return;
        }

        if (!usuarioSelecionado2) {
            exibirMensagem('Selecione um usuário!', 'danger');
            return;
        }

        payload = {
            grafico: "graf2",
            meses: mesesSelecionados2,
            ano: anoSelecionado2,
            user: usuarioSelecionado2
        };
    }

    if (selecaoLimpa) {
        exibirMensagem('Selecione ao menos um mês!', 'danger')
        return;
    }

    $.ajax({
        url: "/atualiza-graficos",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify(payload),
        success: function(resposta) {
            if (payload["grafico"] === "graf1") {
                // carrega grafico 1
                graficoFluxo(resposta.meses, resposta.entradas, resposta.saidas, resposta.saldos);
            } else if (payload["grafico"] === "graf2") {
                // carrega grafico 2
                graficoPatrimonio(resposta.meses, resposta.linha, resposta.barras);
            }
        },
        error: function(erro) {
            exibirMensagem("Nenhum dado foi encontrado.", 'danger');
        }
    });
})

$("#tab1").on("click", function() {
    $("input[type=checkbox]").each(function() {
        if (mesesSelecionados1[this.id] !== undefined) {
            $(this).prop("checked", mesesSelecionados1[this.id]);
        }
    });
    $("#selectAno").val(anoSelecionado1);
    $("#selectUser").val(usuarioSelecionado1);
});

$("#tab2").on("click", function() {
    $("input[type=checkbox]").each(function() {
        if (mesesSelecionados2[this.id] !== undefined) {
            $(this).prop("checked", mesesSelecionados2[this.id]);
        }
    });
    $("#selectAno").val(anoSelecionado2);
    $("#selectUser").val(usuarioSelecionado2);
});

$("#limpar-selecao").on("click", function() {
    $("input[type=checkbox]").each(function() {
        if (mesesSelecionados2[this.id] !== undefined) {
            $(this).prop("checked", false);
        }
    });
});

$("#selecionar-tudo").on("click", function() {
    $("input[type=checkbox]").each(function() {
        if (mesesSelecionados2[this.id] !== undefined) {
            $(this).prop("checked", true);
        }
    });
});





$(function() {
    anoSelecionado1 = $("#selectAno").val();
    anoSelecionado2 = $("#selectAno").val();
    usuarioSelecionado1 = $("#selectUser").val();
    usuarioSelecionado2 = $("#selectUser").val();
    // $.get('/users', function(resposta) {
    //     console.log("Resposta: ", resposta);    
    // });

    // let btn = $("#mes-11");
    // console.log(btn.prop('checked'));
});    


