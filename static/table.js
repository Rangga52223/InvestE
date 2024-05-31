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
      const firstDate = data.dates[0];
      const lastDate = data.dates[data.dates.length - 1];

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

      // Show the table after data is processed
      document.getElementById('stockTable').style.display = 'table';

      // Set the innerHTML of the table body to the constructed HTML string
      tableBody.innerHTML = tableContent;
      stockHeading.innerHTML = `Detail Saham (${firstDate} s.d. ${lastDate})`;
    })
    .catch(error => {
      console.error('Error fetching data:', error);
    });

})();
