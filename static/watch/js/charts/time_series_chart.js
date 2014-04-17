function date_chart(id,url,data_label,xlabel,ylabel,color,) {
    // var d1 = [[1262304000000, 6], [1264982400000, 60], [1267401600000, 2043], [1270080000000, 2198], [1272672000000, 2660], [1275350400000, 2782], [1277942400000, 2430], [1280620800000, 2427], [1283299200000, 2100], [1285891200000, 1214], [1288569600000, 1057], [1291161600000, 1025]];
    jQuery.extend({
        getValues: function(url) {
            var result = null;
            $.ajax({
                url: url,
                type: 'get',
                dataType: 'json',
                async: false,
                success: function(data) {
                    result = data;
                }
            });
           return result;
        }
    });    
    var d1 = $.getValues(url);

    var data1 = [
        { 
            label: data_label, 
            data: d1, 
            color: '#f1553c' 
        }
    ];
 
    $.plot($(id), data1, {
        xaxis: {
            show: true,
            // min: (new Date(2013, 1, 1)).getTime(),
            // max: (new Date(2013, 4, 10)).getTime(),
            mode: "time",
            tickSize: [1, "day"],
            monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            tickLength: 1,
            axisLabel: 'Day',
            axisLabelFontSizePixels: 11
        },
        yaxis: {
            // tickSize: [1,1],
            axisLabel: ylabel,
            axisLabelUseCanvas: true,
            axisLabelFontSizePixels: 11,
            autoscaleMargin: 0.01,

            axisLabelPadding: 5,
            minTickSize: 1,
            transform:function(y){return y.toFixed();}
        },
        series: {
            lines: {
                show: true, 
                fill: true,
                fillColor: { colors: [ { opacity: 0.5 }, { opacity: 0.2 } ] },
                lineWidth: 1.5
            },
            points: {
                show: true,
                radius: 2.5,        
                fill: true,
                fillColor: color,
                symbol: "circle",
                lineWidth: 1.1
            }
        },
       grid: { hoverable: true, clickable: true },
        legend: {
            show: false
        }
    });

    function showTooltip(x, y, contents) {
        $('<div id="tooltip" class="chart-tooltip">' + contents + '</div>').css( {
            position: 'absolute',
            display: 'none',
            top: y - 46,
            left: x - 9,
            'z-index': '9999',
            opacity: 0.9
        }).appendTo("body").fadeIn(200);
    }

    var previousPoint = null;
    $(id).bind("plothover", function (event, pos, item) {
        $("#x").text(pos.x.toFixed(2));
        $("#y").text(pos.y.toFixed(2));

        if ($(id).length > 0) {
            if (item) {
                if (previousPoint != item.dataIndex) {
                    previousPoint = item.dataIndex;
                    
                    $("#tooltip").remove();
                    var x = item.datapoint[0].toFixed(2),
                        y = item.datapoint[1].toFixed(2);
                    
                    showTooltip(item.pageX, item.pageY,
                                item.series.label + " " + "<strong>" + y + "</strong>");
                }
            }
            else {
                $("#tooltip").remove();
                previousPoint = null;            
            }
        }
    });

    $(id).bind("plotclick", function (event, pos, item) {
        if (item) {
            $("#clickdata").text("You clicked point " + item.dataIndex + " in " + item.series.label + ".");
            plot.highlight(item.series, item.datapoint);
        }
    });
};