const $canvas = $("#grafico2");
let grafico = null;

export function graficoPatrimonio(dadosMeses, dadosLinha, dadosBarras) {
    const formatarReais = (valor) => {
        if (valor === null || valor === undefined) return '';
        return 'R$ ' + valor.toLocaleString('pt-BR', { 
            minimumFractionDigits: 2, 
            maximumFractionDigits: 2 
        });
    };

    const datasetsDoGrafico = [];

    datasetsDoGrafico.push({
        type: 'line',
        label: 'Patrimônio',
        data: dadosLinha,
        borderColor: 'rgba(54, 162, 235, 1)',
        backgroundColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 2,
        tension: 0.3,
        order: 0,
        datalabels: {
            align: 'top',
            anchor: 'end',
            formatter: function(value) { return formatarReais(value); },
            font: { weight: 'bold' },
            color: '#0056b3'
        }
    });

    $.each(dadosBarras, function(index, barra) {
        datasetsDoGrafico.push({
            type: 'bar',
            label: barra.label,
            data: barra.data,
            backgroundColor: barra.backgroundColor,
            borderColor: barra.borderColor,
            borderWidth: 1,
            order: 1,
            datalabels: {
                anchor: 'end',
                align: 'end',
                formatter: function(value) { return formatarReais(value); },
                font: { weight: 'normal', size: 10 },
                color: '#333'
            }
        });
    });

    console.log(grafico);

    if (grafico !== null) {
        grafico.destroy();
    }

    const ctx = $canvas[0].getContext('2d');
    grafico = new Chart(ctx, {
        type: 'bar',
        plugins: [ChartDataLabels],
        data: {
            labels: dadosMeses,
            datasets: datasetsDoGrafico
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    grace: '20%',
                    ticks: {
                        callback: function(value) {
                            return 'R$ ' + value.toLocaleString('pt-BR');
                        }
                    }
                }
            },
            plugins: {
                legend: { display: true, position: 'bottom' },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let valor = context.parsed.y;
                            let nomeVariavel = context.dataset.label;
                            return nomeVariavel + ': ' + formatarReais(valor);
                        }
                    }
                }
            }
        }
    });

};