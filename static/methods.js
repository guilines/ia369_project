
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
        var data = {};
        data['operation'] = 'reset';
        jQuery.ajax({   type: "POST",
                        data: data,
                        success: function(data) {
                            var obj = JSON.parse(data);
                            location.reload(); 
                        },
                    });

    });

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
                            //var obj = JSON.parse(data);
                            //console.log(obj);
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
function companyValuesStr(data) {
    $("#company_values_str").jqxListBox({ source: data, width: '900px', height: '100px',});
}

function methodValuesStr(data) {
    $("#method_values_str").jqxListBox({ source: data, width: '900px', height: '100px',});
}


function resultChart(data) {
    console.log(data)
    var data = google.visualization.arrayToDataTable(data.graph);
    //var data = new google.visualization.DataTable();
    //data.addColumn('date','Ano');
    //data.addColumn('number','Brasil');
    //console.log(dt.values);
    //data.addRows(dt.values);

    //data.addColumn('date', 'Day');
    //data.addColumn('number', "Adjustment Price [$]");
    //data.addColumn('number', "Predicted Price [$]");
/*
    for (i=0; i < dt['date'].length; i++) {
        data.addRows([[new Date(dt['date'][i].split('-')), 
                        dt['adj_price'][i], 
                        dt['pred_values'][i]
        
        ]]);
    }

    var cTitle = dt['company_name'] + ' Prediction';*/
    cTitle='Tois';
    var materialOptions = {
        chart : {title: cTitle},
        curveType: 'function',
        width: 900,
        height: 500,
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
   
    var chartDiv = document.getElementById('result_chart'); 
    //var materialChart = new google.charts.Scatter(chartDiv);

    if ($("#chart_type").jqxSwitchButton('checked')){
        var materialChart = new google.charts.Bar(chartDiv);
    } else {
        var materialChart = new google.charts.Scatter(chartDiv);
    }
    //var materialChart = new google.visualization.ScatterChart(chartDiv);
    materialChart.draw(data, materialOptions);

    $("#result_chart_div").show();
}
