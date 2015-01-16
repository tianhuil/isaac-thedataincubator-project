/*
function bindAndRender(myData, maxBirths) {
    global_data = myData;
    nv.addGraph(function() {
        chart = nv.models.lineChart()
                .x(function(d) { return d.year })
                .y(function(d) { return d.births })
                .margin({left: 100})
                .useInteractiveGuideline(true)
                .transitionDuration(350)
                .showLegend(true)
                .showYAxis(true)
                .showXAxis(true)
                .forceY([0, maxBirths]);
        chart.xAxis.axisLabel('Year');
        chart.yAxis.axisLabel("Births");
        d3.select('#chart svg')
                .datum(myData)
                .call(chart);
    });
};

d3.csv("static/birthnames_top_100.csv", function(data, error) {
    var myData = [
        {
            key: "John",
            values: data.filter(function(x) {return x.name == 'John'})
        }];
    max = Math.max.apply(null, data.map(function(x) {return x.births}))
    bindAndRender(myData, max);
})
*/

window.addEventListener('resize', function(event){
        d3.select('#chart svg')
            .call(chart);
});

d3.json("static/model_9-23", function(data, error) {
    plotModelRanges(data)
})

function plotModelRanges(data) {
    global_data = data;
    nv.addGraph(function() {
        chart = nv.models.bulletChart();
        d3.select('#chart svg')
            .datum(transformData(data, 90))
            .transition().duration(1000)
            .call(chart)
        return chart;
    });
}

function transformData(data, centile) {
    key = centile.toString()
    mean = data[key].ret * 100;
    up = mean + 200 * data[key].std;
    down = mean - 200 * data[key].std;

    return {
        title: "Annualized",
        subtitle: "returns",
        ranges: [down, up, 15],
        markers: [data[key].median * 100],
        measures: [data[key].ret * 100]
    };
}

