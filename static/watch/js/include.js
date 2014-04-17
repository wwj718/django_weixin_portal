
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

function date_chart(id,data,xlabel,ylabel) {
    // var d1 = $.getValues(url);
    $.plot($(id), data, {
        xaxis: {
            show: true,
            // min: (new Date(2013, 1, 1)).getTime(),
            // max: (new Date(2013, 4, 10)).getTime(),
            mode: "time",
            tickSize: [1, "day"],
            monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            tickLength: 1,
            axisLabel: 'Day',
            axisLabelFontSizePixels: 11,
            allowDecimals:false,
            timeformat: '%m/%d'
        },
        yaxis: {
            // tickSize: [1,1],
            axisLabel: ylabel,
            axisLabelUseCanvas: true,
            axisLabelFontSizePixels: 11,
            autoscaleMargin: 0.01,
            axisLabelPadding: 5,
            minTickSize: 1,
            allowDecimals:false
            // transform:function(y){return y.toFixed();}
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
                fillColor: '#ffffff',
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
                    var x = item.datapoint[0].toFixed(0),
                        y = item.datapoint[1].toFixed(0);
                    
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


var today = new Date();
var two_week_ago = new Date((today-14*86400*1000));
var today_str = $.datepicker.formatDate('yymmdd', today);
var two_week_ago_str = $.datepicker.formatDate('yymmdd', two_week_ago);

function render_individual(){
    var url = '/watch/get/?d_n=individual&m_n=new_count&min_dt='+two_week_ago_str+'&max_dt='+today_str;
    var id='#chart_new_individual';
    var data_label = '新增个人';
    var xlabel = '日期';
    var ylabel = '新增数量';
    var color = '#f1553c';
    var data1 = {
        data:$.getValues(url),
        color:color,
        label:data_label
    }
    date_chart(id,[data1],xlabel,ylabel);
};
// render_individual();

function render_company(){
    var url = '/watch/get/?d_n=company&m_n=new_count&min_dt='+two_week_ago_str+'&max_dt='+today_str;
    var id='#chart_new_company';
    var data_label = '新增企业';
    var xlabel = '日期';
    var ylabel = '新增数量';
    var color = '#f1553c';
    var data1 = {
        data:$.getValues(url),
        color:color,
        label:data_label
    }
    date_chart(id,[data1],xlabel,ylabel);
};
// render_company();
function render_artist(){
    var url = '/watch/get/?d_n=artist&m_n=new_count&min_dt='+two_week_ago_str+'&max_dt='+today_str;
    var id='#chart_new_artist';
    var data_label = '新增艺术家';
    var xlabel = '日期';
    var ylabel = '新增数量';
    var color = '#f1553c';
    var data1 = {
        data:$.getValues(url),
        color:color,
        label:data_label
    }
    date_chart(id,[data1],xlabel,ylabel);
};

// render_artist();   
 
function render_artwork(){
    var url = '/watch/get/?d_n=artwork&m_n=new_count&min_dt='+two_week_ago_str+'&max_dt='+today_str;
    var id='#chart_new_artwork';
    var data_label = '新增艺术品';
    var xlabel = '日期';
    var ylabel = '新增数量';
    var color = '#f1553c';
    var data1 = {
        data:$.getValues(url),
        color:color,
        label:data_label
    }
    date_chart(id,[data1,],xlabel,ylabel);
};
// render_artwork();
function render_cert(){
    var url_cert_all = '/watch/modelfilter/certificate/?min_dt='+two_week_ago_str+'&max_dt='+today_str;
    var url_cert_uncert = '/watch/modelfilter/certificate/?status="0"&min_dt='+two_week_ago_str+'&max_dt='+today_str;
    var id='#chart_cert';
    var data_label = '鉴定';
    var xlabel = '日期';
    var ylabel = '新增数量';
    var color = '#f1553c';
    var data_all;
    var data1 = {
        data:$.getValues(url_cert_all),
        color:'#46bb00',
        label:'新增作品'
    }
    var data2 = {
        data:$.getValues(url_cert_uncert),
        color:'#f1553c',
        label:'未鉴定'
    }

    console.log(url_cert_all);
    console.log(data1);   
    console.log(data2);   
    date_chart(id,[data1,data2],xlabel,ylabel);    
}

