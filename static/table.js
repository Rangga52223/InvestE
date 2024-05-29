/* globals feather:false */

(function () {
    'use strict'
  
    feather.replace({ 'aria-hidden': 'true' })
  
    // Fetch data from the /data endpoint
    fetch('/data')
      .then(response => response.json())
      .then(data => {
        if (data.error) {
          console.error(data.error);
          return;
        }
  
        // Log data to console for debugging
        console.log(data);
  
        // Get the table body element
        var tableBody = document.getElementById('tableBody');
  
        // Initialize an empty HTML string
        let tableContent = '';
  
        // Populate the table with data
        data.dates.forEach((date, index) => {
          tableContent += `
          <tr>
          <td>${date}</td>
          <td>${data.open[index]}</td>
          <td>${data.high[index]}</td>
          <td>${data.close[index]}</td>
          <td>${data.volume[index]}</td>
        </tr>
          `;
        });
  
        // Set the innerHTML of the table body to the constructed HTML string
        tableBody.innerHTML = tableContent;
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  })();
  