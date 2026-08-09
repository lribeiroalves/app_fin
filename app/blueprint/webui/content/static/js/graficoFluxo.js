const $canvasFluxo = $("#grafico1");
let graficoEntradaSaida = null;

const formatarReais = (valor) => {
    if (valor === null || valor === undefined || valor === 0) return '';
    return 'R$ ' + valor.toLocaleString('pt-BR', { 
        minimumFractionDigits: 2, 
        maximumFractionDigits: 2 
    });
};

export function graficoFluxo(dadosMeses, dadosEntradas, dadosSaidas, dadosSaldo) {
    if (graficoEntradaSaida !== null) {
        graficoEntradaSaida.destroy();
    }

    const ctx = $canvasFluxo[0].getContext('2d');
    graficoEntradaSaida = new Chart(ctx, {
        type: 'bar', // Base do gráfico são barras
        plugins: [ChartDataLabels],
        data: {
            labels: dadosMeses,
            datasets: [
                // 1. A LINHA DE SALDO (Desenhada por cima)
                {
                    type: 'line',
                    label: 'Saldo Líquido',
                    data: dadosSaldo,
                    borderColor: '#333', // Linha escura neutra
                    borderWidth: 2,
                    tension: 0.3,
                    order: 0,
                    // Magia das cores dinâmicas nos pontos da linha
                    pointBackgroundColor: function(context) {
                        let valor = context.dataset.data[context.dataIndex];
                        return valor < 0 ? 'rgba(255, 99, 132, 1)' : 'rgba(75, 192, 192, 1)';
                    },
                    pointBorderColor: '#fff',
                    pointRadius: 6, // Bolinhas um pouco maiores
                    datalabels: {
                        align: function(context) {
                            let valor = context.dataset.data[context.dataIndex];
                            return valor >= 0 ? 'top' : 'bottom';
                        },
                        anchor: 'center', 
                        offset: 8, 
                        backgroundColor: 'rgba(255, 255, 255, 0.75)',
                        borderRadius: 4,
                        padding: 2,
                        formatter: function(value) { return formatarReais(value); },
                        color: function(context) {
                            let valor = context.dataset.data[context.dataIndex];
                            return valor < 0 ? '#d9534f' : '#28a745'; 
                        },
                        font: { weight: 'bold', size: 11 }
                    }
                },
                // 2. BARRA DE ENTRADAS
                {
                    type: 'bar',
                    label: 'Entradas',
                    data: dadosEntradas,
                    backgroundColor: 'rgba(75, 192, 192, 0.6)', // Verde suave
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1,
                    order: 1,
                    datalabels: {
                        anchor: 'end',
                        align: 'top', 
                        offset: 2,
                        formatter: function(value) { return formatarReais(value); },
                        font: { size: 10 },
                        color: '#666'
                    }
                },
                // 3. BARRA DE SAÍDAS
                {
                    type: 'bar',
                    label: 'Saídas',
                    data: dadosSaidas,
                    backgroundColor: 'rgba(255, 99, 132, 0.6)', // Vermelho suave
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1,
                    order: 1,
                    datalabels: {
                        anchor: 'end',
                        align: 'top', 
                        offset: 2,
                        formatter: function(value) { return formatarReais(value); },
                        font: { size: 10 },
                        color: '#666'
                    }
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    // Importante: Não usar beginAtZero se você pode ter saldo negativo, 
                    // o Chart.js criará o eixo negativo automaticamente.
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
                            return context.dataset.label + ': ' + formatarReais(valor);
                        }
                    }
                }
            }
        }
    });
};