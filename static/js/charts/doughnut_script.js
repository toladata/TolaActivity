var doughnutFunction = function(data, tolaDoughnutColors){
    var ctx = document.getElementById(data.component_id);
    var tolaDoughnutChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.labels,
            datasets: [{
                label: "placeholder", // user input axis label
                data: data.data_set,
                backgroundColor: tolaDoughnutColors,
                borderColor: tolaDoughnutColors,
                borderWidth: 1,
            }]
        },
        options: {
            legend: {
                display: true,
                labels: {
                    boxWidth: 10,
                }
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true,
                    }
                }]
            },
            responsive: true,
            maintainAspectRatio: true
            //add options relating to legend generation
        }
    });
};