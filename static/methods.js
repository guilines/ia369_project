$(document).ready(function() {
    createWidgets();
	$("#result_chart_div").hide();
	$("#evaluate_div").hide();
	$("#reset").hide();
	$("#thanks_div").hide();

    $('#reset').on('click', function () {
        location.reload();
    });

	$('#start').on('click', function () {
        var data = {};
        data['operation'] = 'start';
        jQuery.ajax({   type: "POST",
                        dataType: "json",
                        data: JSON.stringify(data),
                        success: function(data) {
	                        next_graph(data);
                        },
                    });
    });

    $("#eval_1").on('checked',function () {
        $('#eval_1').jqxRadioButton('disable');
        $("#eval_1").jqxRadioButton('uncheck');
        $("#result_chart_div").hide();

        var data = {};
        data['operation'] = 'next_graph';
        data['selected'] = 'graph1'
        jQuery.ajax({   type: "POST",
                        dataType: "json",
                        data: JSON.stringify(data),
                        success: function(data) {
                            if (data.stop) {
                                finishTest();
                            } else {
	                        next_graph(data);
	                        }
                        },
                    });
    });

    $("#eval_2").on('checked',function () {
        $('#eval_2').jqxRadioButton('disable');
        $("#eval_2").jqxRadioButton('uncheck');
        $("#result_chart_div").hide();

        var data = {};
        data['operation'] = 'next_graph';
        data['selected'] = 'graph2'
        jQuery.ajax({   type: "POST",
                        dataType: "json",
                        data: JSON.stringify(data),
                        success: function(data) {
	                        if (data.stop) {
                                finishTest();
                            } else {
	                        next_graph(data);
	                        }
                        },
                    });
    });
});

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

    $("#eval_1").jqxRadioButton({
        width: '150',
        height: '25'
    });

    $("#eval_2").jqxRadioButton({
        width: '150',
        height: '25'
    });

	$("#evaluate").jqxRating({
        width: '150',
        height: '25'
    });
    $("#evaluate").hide();

}

function finishTest(data) {
    $("#result_chart_div").hide();
	$("#result_chart2_div").hide();
	$("#evaluate_div").hide();

    $("#reset").show();
	$("#thanks_div").show();
}

function next_graph(data) {
	$("#desc_div").hide();
	$("#start").hide();
	$("#evaluate_div").hide();


    $("#result_chart1").attr('src','');
	$("#result_chart2").attr('src','');

	$("#result_chart1").attr('src',data.graph1);
	$("#result_chart2").attr('src',data.graph2);
	$('#eval_1').jqxRadioButton('enable');
	$('#eval_2').jqxRadioButton('enable');

	$("#result_chart_div").show();


}