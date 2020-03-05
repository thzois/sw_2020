function generate_world_map(filename) {
    let continents_data;
    var lat_lon_continents = [{
          "title": "North America",
          "latitude": 39.563353,
          "longitude": -99.316406,
          "width": 80,
          "height": 80
        },
        {
          "title": "South America",
          "latitude": 0.563353,
          "longitude": -55.316406,
          "width": 40,
          "height": 40
        },
        {
          "title": "Europe",
          "latitude": 54.896104,
          "longitude": 19.160156,
          "width": 50,
          "height": 50
        }, {
          "title": "Asia",
          "latitude": 47.212106,
          "longitude": 103.183594,
          "width": 100,
          "height": 100
        }, {
          "title": "Africa",
          "latitude": 11.081385,
          "longitude": 21.621094,
          "width": 70,
          "height": 70
        },
        {
          "title": "Oceania",
          "latitude": -10.7359,
          "longitude": 130.0188,
          "width": 20,
          "height": 20
        }];
    $.ajax({
        url: 'results/world/' + filename,
        async: false,
        dataType: 'json',
        success: function (data) {
            continents_data = data;
        },
        error: function () {
            alert("Could not load file: " + filename);
        }
    });
    am4core.ready(function() {

        // Themes begin
        am4core.useTheme(am4themes_animated);
        // Themes end

        // Create map instance
        var chart = am4core.create("world_map", am4maps.MapChart);

        // Set map definition
        chart.geodata = am4geodata_continentsLow;

        // Set projection
        chart.projection = new am4maps.projections.Miller();

        // Create map polygon series
        var polygonSeries = chart.series.push(new am4maps.MapPolygonSeries());
        polygonSeries.exclude = ["antarctica"];
        polygonSeries.useGeodata = true;

        // Create an image series that will hold pie charts
        var pieSeries = chart.series.push(new am4maps.MapImageSeries());

        var pieTemplate = pieSeries.mapImages.template;
        pieTemplate.propertyFields.latitude = "latitude";
        pieTemplate.propertyFields.longitude = "longitude";

        var pieChartTemplate = pieTemplate.createChild(am4charts.PieChart);
        pieChartTemplate.adapter.add("data", function(data, target) {
          if (target.dataItem) {
            return target.dataItem.dataContext.pieData;
          }
          else {
            return [];
          }
        });

        pieChartTemplate.propertyFields.width = "width";
        pieChartTemplate.propertyFields.height = "height";
        pieChartTemplate.horizontalCenter = "middle";
        pieChartTemplate.verticalCenter = "middle";

        var pieTitle = pieChartTemplate.titles.create();
        pieTitle.text = "{title}";

        var pieSeriesTemplate = pieChartTemplate.series.push(new am4charts.PieSeries);
        pieSeriesTemplate.dataFields.category = "category";
        pieSeriesTemplate.dataFields.value = "value";
        pieSeriesTemplate.labels.template.disabled = true;
        pieSeriesTemplate.ticks.template.disabled = true;
        pieSeries.data = [];

        for (let i = 0; i < continents_data.length; i++) {
            for (let j = 0; j < lat_lon_continents.length; j++) {
                if (continents_data[i].name === lat_lon_continents[j]['title']) {
                    console.log(continents_data[i].name);
                    pieSeries.data.push({
                        "title": continents_data[i].name,
                        "latitude": lat_lon_continents[j]['latitude'],
                        "longitude": lat_lon_continents[j]['longitude'],
                        "width": lat_lon_continents[j]['width'],
                        "height": lat_lon_continents[j]['height'],
                        "pieData": [
                            {
                                "category": "Positive tweets",
                                "value": continents_data[i].positive_tweets_count
                            },
                            {
                                "category": "Negative tweets",
                                "value": continents_data[i].negative_tweets_count
                            },
                            {
                                "category": "Neutral tweets",
                                "value": continents_data[i].neutral_tweets_count
                            },
                        ]
                    })
                }
            }
        }


    }); // end am4core.ready()
}


// MAP WITH COUNTRIES AND PIECHARTS

//     am4core.ready(function() {
//
//     // Themes begin
//     am4core.useTheme(am4themes_animated);
//     // Themes end
//
//     var chart = am4core.create("world_map", am4maps.MapChart);
//     chart.seriesContainer.draggable = false;
//     chart.seriesContainer.resizable = false;
//
//     try {
//         chart.geodata = am4geodata_worldHigh;
//     }
//     catch (e) {
//         chart.raiseCriticalError(new Error("Map geodata could not be loaded. Please download the latest <a href=\"https://www.amcharts.com/download/download-v4/\">amcharts geodata</a> and extract its contents into the same directory as your amCharts files."));
//     }
//
//     chart.projection = new am4maps.projections.Mercator();
//
//     // zoomout on background click
//     chart.chartContainer.background.events.on("hit", function () { zoomOut() });
//
//     var colorSet = new am4core.ColorSet();
//     var morphedPolygon;
//
//     // map polygon series (countries)
//     var polygonSeries = chart.series.push(new am4maps.MapPolygonSeries());
//     polygonSeries.useGeodata = true;
//     // specify which countries to include
//     // polygonSeries.include = countries_abbreviations;
//     polygonSeries.data = countries_data;
//     // country area look and behavior
//     var polygonTemplate = polygonSeries.mapPolygons.template;
//     polygonTemplate.strokeOpacity = 1;
//     polygonTemplate.stroke = am4core.color("#ffffff");
//     polygonTemplate.fillOpacity = 0.5;
//     polygonTemplate.tooltipText = "{name}: {positivity}% positivity (out of {tweets_count} tweets)";
//
//     // desaturate filter for countries
//     var desaturateFilter = new am4core.DesaturateFilter();
//     desaturateFilter.saturation = 0.25;
//     polygonTemplate.filters.push(desaturateFilter);
//
//     // take a color from color set
//     polygonTemplate.adapter.add("fill", function (fill, target) {
//         return colorSet.getIndex(target.dataItem.index + 1);
//     });
//
//     // set fillOpacity to 1 when hovered
//     var hoverState = polygonTemplate.states.create("hover");
//     hoverState.properties.fillOpacity = 1;
//
//     // what to do when country is clicked
//     polygonTemplate.events.on("hit", function (event) {
//         event.target.zIndex = 1000000;
//         selectPolygon(event.target);
//     });
//
//     // Pie chart
//     var pieChart = chart.seriesContainer.createChild(am4charts.PieChart);
//     // Set width/heigh of a pie chart for easier positioning only
//     pieChart.width = 100;
//     pieChart.height = 100;
//     pieChart.hidden = true; // can't use visible = false!
//
//     // because defauls are 50, and it's not good with small countries
//     pieChart.chartContainer.minHeight = 1;
//     pieChart.chartContainer.minWidth = 1;
//
//     var pieSeries = pieChart.series.push(new am4charts.PieSeries());
//     pieSeries.dataFields.value = "value";
//     pieSeries.dataFields.category = "category";
//     pieSeries.data = [{ value: 100, category: "Positive tweets" }, { value: 20, category: "Negative tweets" }, { value: 10, category: "Neutral tweets" }];
//     var colorSetSlices = new am4core.ColorSet();
//     colorSetSlices.list = [am4core.color("#0582CA"), am4core.color('#E15554'), am4core.color('#f38b4a')];
//     pieSeries.colors = colorSetSlices;
//
//     var dropShadowFilter = new am4core.DropShadowFilter();
//     dropShadowFilter.blur = 4;
//     pieSeries.filters.push(dropShadowFilter);
//
//     var sliceTemplate = pieSeries.slices.template;
//     sliceTemplate.fillOpacity = 1;
//     sliceTemplate.strokeOpacity = 0;
//
//     var activeState = sliceTemplate.states.getKey("active");
//     activeState.properties.shiftRadius = 0; // no need to pull on click, as country circle under the pie won't make it good
//
//     var sliceHoverState = sliceTemplate.states.getKey("hover");
//     sliceHoverState.properties.shiftRadius = 0; // no need to pull on click, as country circle under the pie won't make it good
//
//     // we don't need default pie chart animation, so change defaults
//     var hiddenState = pieSeries.hiddenState;
//     hiddenState.properties.startAngle = pieSeries.startAngle;
//     hiddenState.properties.endAngle = pieSeries.endAngle;
//     hiddenState.properties.opacity = 0;
//     hiddenState.properties.visible = false;
//
//     // series labels
//     var labelTemplate = pieSeries.labels.template;
//     labelTemplate.nonScaling = true;
//     labelTemplate.fill = am4core.color("#FFFFFF");
//     labelTemplate.fontSize = 10;
//     labelTemplate.background = new am4core.RoundedRectangle();
//     labelTemplate.background.fillOpacity = 0.9;
//     labelTemplate.padding(4, 9, 4, 9);
//     labelTemplate.background.fill = am4core.color("#7678a0");
//
//     // we need pie series to hide faster to avoid strange pause after country is clicked
//     pieSeries.hiddenState.transitionDuration = 200;
//
//     // country label
//     var countryLabel = chart.chartContainer.createChild(am4core.Label);
//     // countryLabel.text = "Select a country";
//     countryLabel.fill = am4core.color("#7678a0");
//     countryLabel.fontSize = 40;
//
//     countryLabel.hiddenState.properties.dy = 1000;
//     countryLabel.defaultState.properties.dy = 0;
//     countryLabel.valign = "middle";
//     countryLabel.align = "right";
//     countryLabel.paddingRight = 50;
//     countryLabel.hide(0);
//     countryLabel.show();
//
//     // select polygon
//     function selectPolygon(polygon) {
//         if (morphedPolygon != polygon) {
//             var animation = pieSeries.hide();
//             if (animation) {
//                 animation.events.on("animationended", function () {
//                     morphToCircle(polygon);
//                 })
//             }
//             else {
//                 morphToCircle(polygon);
//             }
//         }
//     }
//
//     // fade out all countries except selected
//     function fadeOut(exceptPolygon) {
//         for (var i = 0; i < polygonSeries.mapPolygons.length; i++) {
//             var polygon = polygonSeries.mapPolygons.getIndex(i);
//             if (polygon != exceptPolygon) {
//                 polygon.defaultState.properties.fillOpacity = 0.5;
//                 polygon.animate([{ property: "fillOpacity", to: 0.5 }, { property: "strokeOpacity", to: 1 }], polygon.polygon.morpher.morphDuration);
//             }
//         }
//     }
//
//     function zoomOut() {
//         if (morphedPolygon) {
//             pieSeries.hide();
//             morphBack();
//             fadeOut();
//             countryLabel.hide();
//             morphedPolygon = undefined;
//         }
//     }
//
//     function morphBack() {
//         if (morphedPolygon) {
//             morphedPolygon.polygon.morpher.morphBack();
//             var dsf = morphedPolygon.filters.getIndex(0);
//             dsf.animate({ property: "saturation", to: 0.25 }, morphedPolygon.polygon.morpher.morphDuration);
//         }
//     }
//
//     function morphToCircle(polygon) {
//
//
//         var animationDuration = polygon.polygon.morpher.morphDuration;
//         // if there is a country already morphed to circle, morph it back
//         morphBack();
//         // morph polygon to circle
//         polygon.toFront();
//         polygon.polygon.morpher.morphToSingle = true;
//         var morphAnimation = polygon.polygon.morpher.morphToCircle();
//
//         polygon.strokeOpacity = 0; // hide stroke for lines not to cross countries
//
//         polygon.defaultState.properties.fillOpacity = 1;
//         polygon.animate({ property: "fillOpacity", to: 1 }, animationDuration);
//
//         // animate desaturate filter
//         var filter = polygon.filters.getIndex(0);
//         filter.animate({ property: "saturation", to: 1 }, animationDuration);
//
//         // save currently morphed polygon
//         morphedPolygon = polygon;
//
//         // fade out all other
//         fadeOut(polygon);
//
//         // hide country label
//         countryLabel.hide();
//
//         if (morphAnimation) {
//             morphAnimation.events.on("animationended", function () {
//                 zoomToCountry(polygon);
//             })
//         }
//         else {
//             zoomToCountry(polygon);
//         }
//     }
//
//     function zoomToCountry(polygon) {
//         var zoomAnimation = chart.zoomToMapObject(polygon, 2.2, true);
//         if (zoomAnimation) {
//             zoomAnimation.events.on("animationended", function () {
//                 showPieChart(polygon);
//             })
//         }
//         else {
//             showPieChart(polygon);
//         }
//     }
//
//
//     function showPieChart(polygon) {
//         polygon.polygon.measure();
//         var radius = polygon.polygon.measuredWidth / 2 * polygon.globalScale / chart.seriesContainer.scale;
//         pieChart.width = radius * 2;
//         pieChart.height = radius * 2;
//         pieChart.radius = radius;
//
//         var centerPoint = am4core.utils.spritePointToSvg(polygon.polygon.centerPoint, polygon.polygon);
//         centerPoint = am4core.utils.svgPointToSprite(centerPoint, chart.seriesContainer);
//
//         pieChart.x = centerPoint.x - radius;
//         pieChart.y = centerPoint.y - radius;
//
//         var fill = polygon.fill;
//         var desaturated = fill.saturate(0.3);
//         for (var i = 0; i < pieSeries.dataItems.length; i++) {
//             var dataItem = pieSeries.dataItems.getIndex(i);
//             if (i === 0) {
//                 dataItem.value = polygon.dataItem.dataContext.positive_percentage;
//             } else if (i === 1) {
//                 dataItem.value = polygon.dataItem.dataContext.negative_percentage;
//             } else if (i === 2) {
//                 dataItem.value = polygon.dataItem.dataContext.neutral_percentage;
//             }
//             dataItem.slice.fill = colorSetSlices[i];
//
//             dataItem.label.background.fill = desaturated;
//             dataItem.tick.stroke = fill;
//         }
//
//         pieSeries.show();
//         pieChart.show();
//
//         countryLabel.text = "{name}";
//         countryLabel.dataItem = polygon.dataItem;
//         countryLabel.fill = desaturated;
//         countryLabel.show();
//     }
//
//
//     });
// } // end am4core.ready()



// BARCHART CODE

    // var myChart = new Chart(ctx, {
    //                             responsive: true,
    //                             type: 'horizontalBar',
    //                             data: {
    //                                 labels: countries,
    //                                 datasets: [
    //                                     {
    //                                         data: number_of_tweets,
    //                                         label: "Bars",
    //                                         backgroundColor: "#f38b4a",
    //                                         borderColor: "#f38b4a"
    //                                     }
    //                                 ]
    //                             },
    //                             options: {
    //                                 title: {
    //                                     display: true,
    //                                     text: "Number of tweets per country"
    //                                 },
    //                                 legend: {
    //                                     display: false
    //                                 },
    //                                 tooltips: {
    //                                     callbacks: {
    //                                         label: function(tooltipItem) {
    //                                             return tooltipItem.xLabel;
    //                                         }
    //                                     }
    //                                 },
    //                                 scales: {
    //                                     yAxes: [{
    //                                         ticks: {
    //                                             fontSize: 12,
    //                                             beginAtZero: true
    //                                         },
    //                                         scaleLabel: {
    //                                             display: true,
    //                                             labelString: "Countries",
    //                                         }
    //                                     }],
    //                                     xAxes: [{
    //                                         scaleLabel: {
    //                                             display: true,
    //                                             labelString: "Number of tweets"
    //                                         }
    //                                     }]
    //                                 }
    //                             }
    //                         });
    // var mapData = [];
    // for (var country in countries_tweets) {
    //     var color;
    //     if (countries_tweets[country] > 500) {
    //         color = chart.colors.getIndex(4);
    //     } else {
    //         color = chart.colors.getIndex(0);
    //     }
    //     mapData.push({"name": country, "value": countries_tweets[country], "color": color});
    // }
