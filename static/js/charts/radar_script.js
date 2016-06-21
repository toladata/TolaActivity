var radarFunction = function(data, color_count, color_palette){
    var ctx = document.getElementById("tolaRadarChart");

    var tolaRadarColors = tolafiedColor(color_palette,color_count);
    var tolaRadarChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['1', '5', '10'], //data.labels}}
            datasets: [{
                label: '# of Things', // user input axis label
                data: data,
                backgroundColor: tolaRadarColors,
                borderColor: tolaRadarColors,
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