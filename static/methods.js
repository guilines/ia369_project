
var tabs = ['A','B','C','D','E','F','G'];

$(document).ready(function() {
    google.charts.load('current', {'packages':['line', 'corechart', 'scatter','bar']});
    //google.charts.setOnLoadCallback(drawChart);
    createWidgets();
    for (i=0;i<tabs.length;i++) {
        $("#"+tabs[i]+"_series_div").hide();
    };
	$("#apply_div").hide();
	$("#chart_type_div").hide();
	$("#result_chart_div").hide();
	$("#reset").hide();

    $('#reset').on('click', function () {
        $("#desc_div").hide();
	    $("#start").hide();
        for (i=0;i<tabs.length;i++) {
            $("#"+tabs[i]+"_series_div").show();
        };
	    $("#chart_type_div").show();
	    $("#apply_div").show();
	    $("#result_chart_div").hide();
	    $("#reset").hide();
    });


/*    $('#reset').on('click', function () {
        var data = {};
        data['operation'] = 'reset';
        jQuery.ajax({   type: "POST",
                        data: data,
                        success: function(data) {
                            var obj = JSON.parse(data);
                            location.reload(); 
                        },
                    });

    });*/

	$('#start').on('click', function () {
        var data = {};
        data['operation'] = 'start';
        jQuery.ajax({   type: "POST",
                        dataType: "json",
                        data: JSON.stringify(data),
                        success: function(data) {
	                        $("#desc_div").hide();
	                        $("#start").hide();
                            for (i=0;i<tabs.length;i++) {
                                $("#"+tabs[i]+"_series_div").show();
                            };
	                        $("#chart_type_div").show();
	                        $("#apply_div").show();
                            var obj = JSON.parse(data);
                        },
                    });

    });

	$('#apply').on('click', function () {
        var data = {};
        data['operation'] = 'apply'
        data['plots'] = getLists();
        jQuery.ajax({   type: "POST",
                        dataType: "json",
                        data: JSON.stringify(data),
                        success: function(data) {
                            console.log(data);
                            resultChart(data);
	                        $("#reset").show();
                        },
                    });

    });

});


function getLists() {
    var data = {};
    for (i=0;i<tabs.length;i++) {
        var checkedItems = [];
        var items = $("#"+tabs[i]+"_series").jqxDropDownList('getCheckedItems');
        $.each(items, function (index) {
            checkedItems.push(this.label);
        });      
        data[tabs[i]] = checkedItems;
    }
    return data;
}

function createWidgets() {
	$("#start").jqxButton({
        width: '150',
        height: '25',
        theme: 'energyblue'
    });

	$("#reset").jqxButton({
        width: '150',
        height: '25',
        theme: 'energyblue'
    });

	$("#apply").jqxButton({
        width: '150',
        height: '25',
        theme: 'energyblue'
    });

    $("#chart_type").jqxSwitchButton({
        width: '150',
        height: '25',
        theme: 'energyblue',
        onLabel: 'Bar Plot',
        offLabel: 'Scatter Plot'
    });

    var sources = []
    var data = {};
    data['operation'] = 'getTabsNames'
    jQuery.ajax({   type: "POST",
                    dataType: "json",
                    data: JSON.stringify(data),
                    success: function(data) {
                        sources=data.names;
                        console.log(sources);
                        createTabs(sources);
                    },
    });

}


function createTabs(sources) {
    var default_width = '600'
    var default_heigth = '35'

    for (i=0;i<tabs.length;i++) {
        $("#"+tabs[i]+"_series").jqxDropDownList({
            source: sources[i],
            width: default_width,
            height: default_heigth,
            checkboxes: true
        });
    };

}

function resultChart(data) {
    console.log(data)
    var data = google.visualization.arrayToDataTable(data.graph);
    
    cTitle='Resultado';
    var scatterOptions = {
        chart : {title: cTitle},
        curveType: 'function',
        width: 1200,
        height: 700,
        /*series: {
            0:{color: 'black', visibleInLegend: true, lineWidth: 0, pointSize: 2, 
                pointsVisible: true},
            1:{color: 'red', visibleInLegend: true, lineWidth: 2, pointSize: 0, 
                pointsVisible: false }
        },*/
        backgroundColor: '#f1f8e9',
        explorer: { actions: ['dragToZoom', 'rightClickToReset'], axis: 'horizontal' },
        legend: { position: 'bottom' }
    };

    var barOptions = {
        chart : {title: cTitle},
        curveType: 'function',
        width: 1200,
        height: 700,
        bars: 'horizontal', // Required for Material Bar Charts.
        backgroundColor: '#f1f8e9',
        explorer: { actions: ['dragToZoom', 'rightClickToReset'], axis: 'horizontal' },
        legend: { position: 'bottom' }
    };

    var chartDiv = document.getElementById('result_chart'); 

    if ($("#chart_type").jqxSwitchButton('checked')){
        var materialChart = new google.charts.Bar(chartDiv);
        materialChart.draw(data, barOptions);
    } else {
        var materialChart = new google.charts.Scatter(chartDiv);
        materialChart.draw(data, scatterOptions);
        //var materialChart = new google.visualization.ScatterChart(chartDiv);
    }
    for (i=0;i<tabs.length;i++) {
        $("#"+tabs[i]+"_series_div").hide();
    }
    $("#result_chart_div").show();
}
