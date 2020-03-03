function sentiment_gauge(ctx, filename){

    var app_data;
  
    $.ajax({
      url: "results/sentiment/" + filename,
      async: false,
      dataType: 'json',
      success: function (data) {
        app_data = data;
      },
      error: function () {
        alert("Could not load file: " + filename);
      }
    });

    aggr_data = [ app_data["positive_percentage"].toFixed(2), 
                  app_data["neutral_percentage"].toFixed(2),
                  app_data["negative_percentage"].toFixed(2),
    ];
    var chart = new Chart(ctx, {
                                  type: 'doughnut',
                                  responsive: true,
                                  data: {
                                      labels: ["Positive", "Neutral", "Negative"],
                                      datasets: [{
                                          label: "My First dataset",
                                          backgroundColor: ['#36A2EB', '#FFCD56', '#ff6384'],
                                          borderColor: '#fff',
                                          data: aggr_data,
                                      }]
                                  },
                                  options: {
                                    title: { 
                                      display: true,
                                      text: "Feelings for all the event days"
                                    },
                                    tooltips: {
                                      callbacks: {
                                        label: function(t, d) {
                                          return d["labels"][t.index] + ": " + aggr_data[t.index] + "%";
                                        }
                                      }
                                    }
                                  }
                                  // options: {
                                  //     circumference: 1 * Math.PI,
                                  //     rotation: 1 * Math.PI,
                                  //     cutoutPercentage: 70
                                  // }
                              });
}