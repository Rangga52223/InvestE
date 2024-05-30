function fetchPredictions() {
    const ticker = document.getElementById('tickerSelect').value;
    fetch(`/predict?ticker=${ticker}`)
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('predictionChart').getContext('2d');
            const labels = Array.from({length: data.predictions.length}, (_, i) => {
                const date = new Date();
                date.setDate(date.getDate() + i);
                return date.toISOString().split('T')[0];
            });
            const chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: `Predicted Stock Price for ${ticker} (USD)`,
                        data: data.predictions,
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 2,
                        pointBackgroundColor: 'rgba(75, 192, 192, 1)',
                        fill: false
                    }]
                },
                options: {
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'Date'
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Price (USD)'
                            }
                        }
                    },
                    plugins: {
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return `Price: $${context.raw}`;
                                }
                            }
                        }
                    }
                }
            });
        });
}

// Fetch predictions for the default ticker on page load
window.onload = fetchPredictions;