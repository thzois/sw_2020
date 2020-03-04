function world_barchart(ctx, filename) {

    countries = [];
    number_of_tweets = [];

    $.ajax({
        url: 'results/world/' + filename,
        async: false,
        dataType: 'json',
        success: function (data) {
            let i = 0;
            for (var country_name in data) {
                countries.push(country_name);
                number_of_tweets.push(data[country_name]);
                i+=1;
                if (i === 10) {
                    break
                }
            }
        },
        error: function () {
            alert("Could not load file: " + filename);
        }
    });

    var myChart = new Chart(ctx, {
                                responsive: true,
                                type: 'horizontalBar',
                                data: {
                                    labels: countries,
                                    datasets: [
                                        {
                                            data: number_of_tweets,
                                            label: "Bars",
                                            backgroundColor: "#f38b4a",
                                            borderColor: "#f38b4a"
                                        }
                                    ]
                                },
                                options: {
                                    title: {
                                        display: true,
                                        text: "Number of tweets per country"
                                    },
                                    legend: {
                                        display: false
                                    },
                                    tooltips: {
                                        callbacks: {
                                            label: function(tooltipItem) {
                                                return tooltipItem.xLabel;
                                            }
                                        }
                                    },
                                    scales: {
                                        yAxes: [{
                                            ticks: {
                                                fontSize: 12,
                                                beginAtZero: true
                                            },
                                            scaleLabel: {
                                                display: true,
                                                labelString: "Country",
                                            }
                                        }],
                                        xAxes: [{
                                            scaleLabel: {
                                                display: true,
                                                labelString: "Number of tweets"
                                            }
                                        }]
                                    }
                                }
                            });
}