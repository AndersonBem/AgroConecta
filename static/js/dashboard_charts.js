// Arquivo: static/js/dashboard_charts.js

// Cores da sua paleta (aproximadas para Chart.js)
const PRIMARY_COLOR = '#002D28'; // var(--verde-1)
const SECONDARY_COLOR = '#489372'; // var(--verde-2)
const DANGER_COLOR = '#d74444'; // Para status de alerta

// ======================================
// 1. GRÁFICO DE BARRAS: Sementes por Armazém
// ======================================

const ctx1 = document.getElementById('sementeArmazemChart');

new Chart(ctx1, {
    type: 'bar',
    data: {
        labels: ['Armazém 01', 'Armazém 02', 'Armazém 03', 'Armazém 04'], // Nome dos Armazéns (Vindo do Django)
        datasets: [{
            label: 'Total de Sementes (kg)',
            data: [15000, 22000, 9500, 18000], // Dados de peso (Vindo do Django)
            backgroundColor: SECONDARY_COLOR,
            borderColor: PRIMARY_COLOR,
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        },
        plugins: {
            legend: {
                display: false
            }
        }
    }
});

// ======================================
// 2. GRÁFICO DE ROSCA: Status das Solicitações
// ======================================

const ctx2 = document.getElementById('solicitacoesChart');

new Chart(ctx2, {
    type: 'doughnut',
    data: {
        labels: ['Aprovadas', 'Pendentes', 'Rejeitadas'], // Status (Vindo do Django)
        datasets: [{
            label: 'Nº de Solicitações',
            data: [45, 12, 5], // Contagem de solicitações (Vindo do Django)
            backgroundColor: [
                SECONDARY_COLOR,
                '#ffc107', // Amarelo para Pendente
                DANGER_COLOR
            ],
            hoverOffset: 4
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'bottom',
            }
        }
    }
});


// ======================================
// 3. GRÁFICO DE LINHA: Lotes Entregues ao Tempo
// ======================================

const ctx3 = document.getElementById('lotesTempoChart');

new Chart(ctx3, {
    type: 'line',
    data: {
        labels: ['Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov'], // Meses (Vindo do Django)
        datasets: [{
            label: 'Lotes Entregues',
            data: [3, 5, 8, 7, 12, 15], // Quantidade de lotes (Vindo do Django)
            fill: true,
            backgroundColor: 'rgba(72, 147, 114, 0.2)', // Fundo suave
            borderColor: SECONDARY_COLOR,
            tension: 0.3
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        },
        plugins: {
            legend: {
                display: false
            }
        }
    }
});