(function () {
    'use strict'

    feather.replace({ 'aria-hidden': 'true' })

    fetch('/stockdata')      
    .then(response => response.json())
    .then(data => {
        const data_indo = data[0];
        const data_us = data[1];
        if (data_indo.error || data_us.error) {
            console.error(data_indo.error || data_us.error);
            return;
        }

        console.log(data_indo);
        console.log(data_us);

        var tableIndo = document.getElementById('Indo');
        var tableUs = document.getElementById('Us');

        let tableContentIndo = '';
        let tableContentUs = '';

        data_indo.forEach((stock, index) => {
            tableContentIndo += `
            <tr>
                <td>${stock.dates}</td>
                <td>${stock.emiten}</td>
                <td>${stock.close}</td>
                <td>${stock.volume}</td>
            </tr>
            `;
        });

        data_us.forEach((stock, index) => {
            tableContentUs += `
            <tr>
            <td>${stock.dates}</td>
                <td>${stock.emiten}</td>
                <td>${stock.close}</td>
                <td>${stock.volume}</td>
            </tr>
            `;
        });

        tableIndo.innerHTML = tableContentIndo;
        tableUs.innerHTML = tableContentUs;

        document.getElementById('tableUS').style.display = 'table';
        document.getElementById('tableID').style.display = 'table';
    })
    .catch(error => {
        console.error('Error fetching stock data:', error);
    });
})();
