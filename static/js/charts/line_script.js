var lineFunction = function(data, tolaColor){
    var ctx = document.getElementById("tolaLineChart");
    var tolaLineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['1', '5', '10'], //{{tolaTableData.labels}}
            datasets: [{
                label: '# of Things', // user input axis label
                data: data,
                backgroundColor: [ 
                    '{{tolaColor.0}}',
                    '{{tolaColor.1}}',
                    '{{tolaColor.2}}',
                    '{{tolaColor.3}}',
                    '{{tolaColor.4}}',
                    '{{tolaColor.5}}', //var no_colors = tolaTableData.labels.count, shuffle palette, pop that # of colors from palette to get the array of colors
                ],
                borderColor: [
                    '{{tolaColor.0}}',
                    '{{tolaColor.1}}',
                    '{{tolaColor.2}}',
                    '{{tolaColor.3}}',
                    '{{tolaColor.4}}',
                    '{{tolaColor.5}}',//use the same array of colors
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