var pieFunction = function(data, tolaPieColors){
    var ctx = document.getElementById("tolaPieChart");
    var tolaPieChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['1', '5', '10'], //data.labels
            datasets: [{
                label: '# of Things', // user input axis label
                data: data.data_set,
                backgroundColor: tolaPieColors,
                borderColor: tolaPieColors,
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