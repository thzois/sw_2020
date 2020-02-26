var years = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017];
var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]
              
// Creates a line chart for month comparison between months 
function pie_chart(ctx, filename, title){

  // Get results file 
  var req = new XMLHttpRequest();  
  req.open('GET', 'results/'+filename, false);   
  req.send();  
  if(req.status == 4 || req.status == 200){  
    // Read data and split to lines
    var data = (req.responseText).match(/[^\r\n]+/g);
  }else{
    alert("Could not load file " + filename);
  }

  var metric_per_year = new Array();
  var idx = 0;
  var total = 0;
  // Construct the data for the chart
  // We don't need the first line (headers)
  for (i = 1; i < data.length; i++) {
    metric_per_year[idx] = Number(data[i].split(",")[1]);
    total += metric_per_year[idx];
    idx++;
  }

  var myChart = new Chart(ctx, {
                                responsive: true,
                                type: 'pie',
                                data: {
                                  labels: years,
                                  datasets: [{
                                    backgroundColor: ["#585858", "#f38b4a", "#E5CA1B", "#e8c3b9", "#3e95cd", "#8e5ea2","#3cba9f","#c45850", "#D8D8D8"],
                                    data: metric_per_year
                                  }]
                                },
                                options: {
                                  title: {
                                    display: true,
                                    text: title + total + ")"
                                  },
                                  tooltips: {
                                    callbacks: {
                                      label: function(tooltipItem, data) {
                                        var allData = data.datasets[tooltipItem.datasetIndex].data;
                                        var tooltipLabel = data.labels[tooltipItem.index];
                                        var tooltipData = allData[tooltipItem.index];
                                        var total = 0;
                                        for (var i in allData) {
                                          total += allData[i];
                                        }
                                        var tooltipPercentage = Math.round((tooltipData / total) * 100);
                                        return tooltipLabel + ': ' + tooltipData + ' (' + tooltipPercentage + '%)';
                                      }
                                    }
                                  }
                                }         
                              });
}