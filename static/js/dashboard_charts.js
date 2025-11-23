// static/js/dashboard_charts.js

const PRIMARY_COLOR = '#002D28';   // var(--verde-1)
const SECONDARY_COLOR = '#489372'; // var(--verde-2)
const DANGER_COLOR = '#ee7f25ff';

// Lê os dados do <div id="dashboard-data">
function getChartData() {
    const el = document.getElementById('dashboard-data');
    if (!el) {
        console.warn('Elemento #dashboard-data não encontrado.');
        return null;
    }

    // data-armazem-labels -> dataset.armazemLabels
    const parse = (name) => {
        const raw = el.dataset[name] || '[]';
        try {
            return JSON.parse(raw);
        } catch (e) {
            console.error(`Erro ao parsear ${name}:`, raw, e);
            return [];
        }
    };

    return {
        armazemLabels: parse('armazemLabels'),
        armazemDados:  parse('armazemDados'),
        statusLabels:  parse('statusLabels'),
        statusDados:   parse('statusDados'),
        lotesLabels:   parse('lotesLabels'),
        lotesDados:    parse('lotesDados'),
    };
}

document.addEventListener('DOMContentLoaded', () => {
    const data = getChartData();
    if (!data) return;

    // ================================
    // 1. BARRAS: Sementes por Armazém
    // ================================
    const ctx1 = document.getElementById('sementeArmazemChart');
    if (ctx1) {
        new Chart(ctx1, {
            type: 'bar',
            data: {
                labels: data.armazemLabels,
                datasets: [{
                    label: 'Total de Sementes (kg)',
                    data: data.armazemDados,
                    backgroundColor: SECONDARY_COLOR,
                    borderColor: PRIMARY_COLOR,
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { beginAtZero: true }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }

    // ================================
    // 2. ROSCA: Status das Solicitações
    // ================================
    const ctx2 = document.getElementById('solicitacoesChart');
    if (ctx2) {
        new Chart(ctx2, {
            type: 'doughnut',
            data: {
                labels: data.statusLabels,
                datasets: [{
                    label: 'Nº de Solicitações',
                    data: data.statusDados,
                    backgroundColor: [
                        SECONDARY_COLOR,
                        '#ff2c07ff', // pendente
                        DANGER_COLOR
                    ],
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });
    }

    // =======================================
    // 3. LINHA: Lotes criados nos últimos meses
    // =======================================
    const ctx3 = document.getElementById('lotesTempoChart');
    if (ctx3) {
        new Chart(ctx3, {
            type: 'line',
            data: {
                labels: data.lotesLabels,
                datasets: [{
                    label: 'Lotes Criados',
                    data: data.lotesDados,
                    fill: true,
                    backgroundColor: 'rgba(72, 147, 114, 0.2)',
                    borderColor: SECONDARY_COLOR,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { beginAtZero: true }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }
});
