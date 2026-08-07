var anoSelecionado1 = 0;
var anoSelecionado2 = 0;
var mesesSelecionados2 = {};
var mesesSelecionados1 = {};
var payload = {}

$("input[type=checkbox]").each(function() {
  mesesSelecionados1[this.id] = true;
  mesesSelecionados2[this.id] = true;
});

$("#atualiza-grafico").on("click", function() {
    if ($(".tab-pane.active").attr("id") === "graf1") {
        $("input[type=checkbox]").each(function() {
            mesesSelecionados1[this.id] = $(this).prop("checked");
        });
        anoSelecionado1 = $("#selectAno").val();

        payload = {
            grafico: "graf1",
            meses: mesesSelecionados1,
            ano: anoSelecionado1
        };

    } else if ($(".tab-pane.active").attr("id") === "graf2") {
        $("input[type=checkbox]").each(function() {
            mesesSelecionados2[this.id] = $(this).prop("checked");
        });
        anoSelecionado2 = $("#selectAno").val();

        payload = {
            grafico: "graf2",
            meses: mesesSelecionados2,
            ano: anoSelecionado2
        };
    }

    $.ajax({
        url: "/atualiza-graficos",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify(payload),
        success: function(resposta) {
            if (payload["grafico"] === "graf1") {
                // carrega grafico 1
                console.log("graf1", resposta)
            } else if (payload["grafico"] === "graf2") {
                // carrega grafico 2
                console.log("graf2", resposta)
            }
        },
        error: function(erro) {
            console.log(erro)
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
});

$("#tab2").on("click", function() {
    $("input[type=checkbox]").each(function() {
        if (mesesSelecionados2[this.id] !== undefined) {
            $(this).prop("checked", mesesSelecionados2[this.id]);
        }
    });
    $("#selectAno").val(anoSelecionado2);
});





$(function() {
    anoSelecionado1 = $("#selectAno").val();
    anoSelecionado2 = $("#selectAno").val();
    // $.get('/users', function(resposta) {
    //     console.log("Resposta: ", resposta);    
    // });

    // let btn = $("#mes-11");
    // console.log(btn.prop('checked'));
});    


