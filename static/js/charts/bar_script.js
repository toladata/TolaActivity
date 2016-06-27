var barFunction = function(data, tolaBarColors){
    var ctx = document.getElementById(data.component_id);
    var tolaBarChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [{
                label: '# of Things', // user input axis label
                data: data.data_set,
                backgroundColor: tolaBarColors,
                borderColor: tolaBarColors,
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
            },
            responsive: true,
            maintainAspectRatio: true
            //add options relating to legend generation
        }
    });
};