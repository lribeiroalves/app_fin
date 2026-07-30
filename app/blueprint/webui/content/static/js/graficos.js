const canvas = document.getElementById("graf-resultado");
const labelsResultado = JSON.parse(canvas.dataset.labels);
const valuesResultado = JSON.parse(canvas.dataset.values);

console.log('Teste')
console.log(canvas);
console.log(labelsResultado);
console.log(valuesResultado);

// 1. Definindo a função que estava faltando para formatar os valores
    const formatarReais = (valor) => {
        return 'R$ ' + valor.toLocaleString('pt-BR', { 
            minimumFractionDigits: 2, 
            maximumFractionDigits: 2 
        });
    };



const ctx = canvas.getContext('2d');
const barChart = new Chart(ctx, {
    type: 'bar',
    plugins: [ChartDataLabels],
    data: {
        labels: labelsResultado,
        datasets: [{
            label: '',
            data: valuesResultado,
            backgroundColor: ['rgba(255, 255, 224, 0.6)', 'rgba(255, 182, 193, 0.6)'],
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true,
                grace: '15%',
                ticks: {
                    callback: function(value) {
                        return 'R$ ' + value.toLocaleString('pt-BR');
                    }
                }
            }
        },
        plugins: {
            legend: {
                display: false
            },

            // 1. Configuração do Tooltip (Hover)
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            // Pegamos o valor exato do eixo Y
                            let valor = context.parsed.y;
                            return formatarReais(valor);
                        }
                    }
                },
                
                // 2. Configuração do DataLabels (Texto no topo da barra)
                datalabels: {
                    anchor: 'end',  // Ancora o texto no final da barra (topo)
                    align: 'end',   // Alinha para fora/cima da barra
                    formatter: function(value) {
                        return formatarReais(value);
                    },
                    font: {
                        weight: 'bold'
                    },
                    color: '#333' // Cor do texto
                }
        }
    }
});