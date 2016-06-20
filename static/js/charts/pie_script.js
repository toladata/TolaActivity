var pieFunction = function(data){
    var ctx = document.getElementById("tolaPieChart");
    var tolaPieChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['1', '5', '10'], //{{tolaTableData.labels}}
            datasets: [{
                label: '# of Things', // user input axis label
                data: data,
                backgroundColor: [ 
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)', //var no_colors = tolaTableData.labels.count, shuffle palette, pop that # of colors from palette to get the array of colors
                ],
                borderColor: [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)',//use the same array of colors
                ],
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