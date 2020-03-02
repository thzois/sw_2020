$(document).ready(function () {

    var filename = `barchart_${$('.list-group-1').attr('id')}.json`;
    console.log(filename);
    var sentiments_per_country;
    countries = [];
    number_of_tweets = [];

    $.ajax({
        url: filename,
        async: false,
        dataType: 'json',
        success: function (data) {
            sentiments_per_country = data;
            console.log(sentiments_per_country);
            for (var country_name in data) {
                countries.push(country_name);
                number_of_tweets.push(data[country_name]);
            }
        },
        error: function () {
            alert("Could not load file: " + filename + ".json");
        }
    });

    function addData(chart) {
            chart.data.datasets[0].data.push(0);
            var newwidth = $('.chartAreaWrapper2').width() + 60;
            $('.chartAreaWrapper2').width(newwidth);
    }

    var chartData = {
        labels: countries,
        datasets: [{
            label: "Number of tweets per country",
            data: number_of_tweets,
            backgroundColor: "#f38b4a",
            borderColor: "#f38b4a"
        }]
    };



    $(function () {
        var rectangleSet = false;

        var canvasTest = $('#world_bar');
        var chartTest = new Chart(canvasTest, {
            type: 'bar',
            data: chartData,
            maintainAspectRatio: false,
            responsive: true,
            options: {
                legend: {
                    position: 'top'
                },
                tooltips: {
                    callbacks: {
                        label: function(tooltipItem) {
                            return tooltipItem.yLabel;
                        }
                    }
                },
                scales: {
                    xAxes: [{
                        ticks: {
                            fontSize: 12,
                            // display: true
                        },
                        scaleLabel: {
                            display: true,
                            labelString: "Countries"
                        }
                    }],
                    yAxes: [{
                        ticks: {
                            fontSize: 12,
                            beginAtZero: true
                        },
                        scaleLabel: {
                            display: true,
                            labelString: "Number of tweets"
                        }
                    }]
                },
                animation: {
                    onComplete: function () {
                        if (!rectangleSet) {
                            var scale = window.devicePixelRatio;

                            var sourceCanvas = chartTest.chart.canvas;
                            var copyWidth = chartTest.scales['y-axis-0'].width - 10;
                            var copyHeight = chartTest.scales['y-axis-0'].height + chartTest.scales['y-axis-0'].top + 10;

                            var targetCtx = document.getElementById("axis-world-bar").getContext("2d");

                            targetCtx.scale(scale, scale);
                            targetCtx.canvas.width = copyWidth * scale;
                            targetCtx.canvas.height = copyHeight * scale;

                            targetCtx.canvas.style.width = `${copyWidth}px`;
                            targetCtx.canvas.style.height = `${copyHeight}px`;
                            targetCtx.drawImage(sourceCanvas, 0, 0, copyWidth * scale, copyHeight * scale, 0, 0, copyWidth * scale, copyHeight * scale);

                            var sourceCtx = sourceCanvas.getContext('2d');

                            // Normalize coordinate system to use css pixels.

                            sourceCtx.clearRect(0, 0, copyWidth * scale, copyHeight * scale);
                            rectangleSet = true;
                        }
                    },
                    onProgress: function () {
                        if (rectangleSet === true) {
                            var copyWidth = chartTest.scales['y-axis-0'].width;
                            var copyHeight = chartTest.scales['y-axis-0'].height + chartTest.scales['y-axis-0'].top + 10;

                            var sourceCtx = chartTest.chart.canvas.getContext('2d');
                            sourceCtx.clearRect(0, 0, copyWidth, copyHeight);
                        }
                    }
                }
            }
        });
        addData(chartTest);
    });
});


// var myChart = new Chart(ctxWorldBar, {
//                                 responsive: true,
//                                 type: 'bar',
//                                 data: {
//                                     labels: countries,
//                                     datasets: [
//                                         {
//                                             data: number_of_tweets,
//                                             label: "Bars",
//                                             backgroundColor: "#f38b4a",
//                                             borderColor: "#f38b4a"
//                                         },
//                                         {
//                                             type: "line",
//                                             label: "Line",
//                                             borderColor: "#0582CA",
//                                             fill: true,
//                                             borderWidth: 2,
//                                             data: number_of_tweets,
//                                             pointBackgroundColor: "#0582CA"
//                                         }
//                                     ]
//                                 },
//                                 options: {
//                                     title: {
//                                         display: true,
//                                         text: title
//                                     },
//                                     legend: {
//                                         position: 'top'
//                                     },
//                                     tooltips: {
//                                         callbacks: {
//                                             label: function(tooltipItem) {
//                                                 return tooltipItem.yLabel;
//                                             }
//                                         }
//                                     },
//                                     scales: {
//                                         yAxes: [{
//                                             ticks: custom_ticks,
//                                             scaleLabel: {
//                                                 display: true,
//                                                 labelString: yLabel,
//                                             }
//                                         }],
//                                         xAxes: [{
//                                             scaleLabel: {
//                                                 display: true,
//                                                 labelString: xLabel
//                                             }
//                                         }]
//                                     }
//                                 }
//                             });
//
//
// }