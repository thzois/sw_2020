function sentiment_vs_stock(ctx, filename, title, yLabel, xLabel){

  // Get results file 
  $.getJSON( "results/" + filename, function( data ) {
    // $.each( data, function( key, val ) {
    //   console.log(data);
    // });
  }).fail(function() {
    console.log("Could not load file: " + filename);
  });


  // var years = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017];
  // var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]
              
  // // Construct the JSON for each year 
  // jsonData = {};
  // var metric_months = new Array();
  // var metric_per_year_month = new Array();
  // var idx_year = 0;
  // var idx = 0;

  // colors = ["#f38b4a", "#0582CA", "#963484", "#E5CA1B", "#F8333C", "#3F7D20", "#7B7C7C", "#000000", "#932C2C"]

  // for (i = 1; i < data.length; i++) {

  //   year = String(data[i].split(",")[0]);
    
  //   metric_months[idx] = Number(data[i].split(",")[2]);

  //   idx++;

  //   //Switch year - Construct JSON for chart
  //   if(i%12 == 0 || (year == "2017" && idx == 3)){

  //     jsonData["label"] = year;
  //     jsonData["data"] = metric_months;
  //     jsonData["borderColor"] = colors[idx_year];
  //     jsonData["backgroundColor"] = colors[idx_year];
  //     jsonData["fill"] = false;
  //     jsonData["borderWidth"] = 2;
    

  //     // Hide every line except the first three
  //     if(year != "2009" && year != "2010" && year != "2011"){
  //       jsonData["hidden"] = true;
  //     }

  //     // Change line for the year array and store JSON
  //     metric_per_year_month[idx_year] = jsonData;
  //     idx_year++;

  //     // Reset months array and JSON object
  //     jsonData = {};
  //     metric_months = [];
  //     idx = 0;
  //   }
  // }

  //   // Handle ticks of ratio
  // custom_ticks = {};

  // if(filename.includes("conductance") || filename.includes("bridge") || filename.includes("tpr")){    
  //     custom_ticks["min"] = 0;
  //     custom_ticks["max"] = 1;
  // }

  // custom_ticks["beginAtZero"] = true;

  // var myChart = new Chart(ctx, {
  //                               responsive: true,
  //                               type: 'line',
  //                               data: {
  //                               labels: months,
  //                                   datasets: metric_per_year_month,
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
  //                                       mode: 'label',
  //                                     },
  //                                     scales: {
  //                                       yAxes: [{
  //                                         ticks: custom_ticks,
  //                                         scaleLabel: {
  //                                           display: true,
  //                                           labelString: yLabel
  //                                         }
  //                                       }],
  //                                       xAxes: [{
  //                                         scaleLabel: {
  //                                           display: true,
  //                                           labelString: xLabel
  //                                         }
  //                                       }]
  //                                     } 
  //                                 }
  //                             });
}
