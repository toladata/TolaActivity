var doughnutFunction = function(data, tolaDoughnutColors){
    var ctx = document.getElementById("tolaDoughnutChart");
    var tolaDoughnutChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['1', '5', '10'], //{{tolaTableData.labels}}
            datasets: [{
                label: '# of Things', // user input axis label
                data: data,
                backgroundColor: tolaDoughnutColors,
                borderColor: tolaDoughnutColors,
                borderWidth: 1,
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true,
                    }
                }]
            }
            //add options relating to legend generation
        }
    });
};