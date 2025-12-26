const ctx = document.getElementById('expenseChart').getContext('2d');
new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: ['Food', 'Travel', 'Bills', 'Shopping', 'Others'],
        datasets: [{
            data: [300, 350, 700, 200, 100],
            backgroundColor: ['#00e6b8', '#514a9d', '#ff512f', '#96c93d', '#24c6dc'],
            borderWidth: 0
        }]
    },
    options: {
        plugins: {
            legend: { position: 'bottom' }
        }
    }
});
