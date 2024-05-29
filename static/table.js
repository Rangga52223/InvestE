/* globals Chart:false, feather:false */

(function () {
  'use strict';

  feather.replace({ 'aria-hidden': 'true' });

  // ngambil data dari endpoint api nya flask
  function fetchData(startDate, endDate) {    
    fetch(`/getdata?start_date=${startDate}&end_date=${endDate}`)// ini endpoit nya kayak rule nya ngambil disini
      .then(response => response.json())
      .then(data => {
        if (data.error) {
          console.error(data.error);
          return;
        }

        // Log data to console for debugging
        console.log(data);

        // buat chart nya
        var ctx = document.getElementById('myChart').getContext('2d');
        var myChart = new Chart(ctx, {
          type: 'line',
          data: {
            labels: data.dates,
            datasets: [{
              label: data.emiten,
              data: data.close,  // Use 'close' from the response
              lineTension: 0,
              backgroundColor: 'transparent',
              borderColor: '#007bff',
              borderWidth: 4,
              pointBackgroundColor: '#007bff'
            }]
          },
          options: {
            scales: {
              y: {
                beginAtZero: false
              }
            },
            plugins: {
              legend: {
                display: true
              }
            }
          }
        });
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }

  // Buat nampilin 30hari gess
  function calculateDateRange() {
    var endDate = new Date();
    var startDate = new Date();
    startDate.setDate(endDate.getDate() - 1825);

    return {
      startDate: startDate.toISOString().split('T')[0],
      endDate: endDate.toISOString().split('T')[0]
    };
  }

  document.addEventListener('DOMContentLoaded', function () {
    const emtnSelect = document.getElementById('emtn');
    const timeSelect = document.getElementById('time');
    
    // Retrieve the selected option from localStorage
    const savedEmtn = localStorage.getItem('selectedEmtn');
    const savedTime = localStorage.getItem('selectedTime');
    
    if (savedEmtn) {
        emtnSelect.value = savedEmtn;
    }

    if (savedTime) {
      timeSelect.value = savedTime;
  }

    // Save the selected option to localStorage when the form is submitted
    document.getElementById('stockForm').addEventListener('submit', function () {
        const selectedEmtn = emtnSelect.value;
        const selectedTime = timeSelect.value;
        localStorage.setItem('selectedEmtn', selectedEmtn);
        localStorage.setItem('selectedTime', selectedTime);
    });
  });


  // Fetch initial data for the last 30 days
  var dateRange = calculateDateRange();
  fetchData(dateRange.startDate, dateRange.endDate);
})();
