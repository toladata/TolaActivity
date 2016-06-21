var doughnutFunction = function(data, color_count, color_palette){
    var ctx = document.getElementById("tolaDoughnutChart");
    var tolaDoughnutColors = tolafiedColor(color_palette,color_count); // this should be revised to be something
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