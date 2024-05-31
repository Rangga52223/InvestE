let chart = null;
spinner.style.display = 'none'; 

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
            
            // Hapus chart sebelumnya
            if (chart) {
                chart.destroy();
            }

            // Create a new chart instance
            chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: `Predicted Stock Price for ${ticker} (Rp.)`,
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
                                text: 'Price (Rp.)'
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
            spinner.style.display = 'none'; 

        });

        var spinner = document.getElementById('spinner');
        spinner.style.display = 'block'; // Show the spinner
        chart = null

        document.addEventListener('DOMContentLoaded', () => {
            fetchPredictions();
            document.getElementById('tickerSelect').addEventListener('change', fetchPredictions);
        });


}

