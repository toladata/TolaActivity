var polarFunction = function(data){
    var ctx = document.getElementById("tolaPolarChart");
    var tolaPolarChart = new Chart(ctx, {
        type: 'polar',
        data: {
            datasets: [{
	        data: data,
	        backgroundColor: [
	            "#FF6384",
	            "#4BC0C0",
	            "#FFCE56",
	            "#E7E9ED",
	            "#36A2EB"
	        ],
	        label: 'My dataset' // for legend
		    }],
		    labels: [
		        "Red",
		        "Green",
		        "Yellow",
		        "Grey",
		        "Blue"
		    ]},
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