$(document).ready(function () {
    $("#surveyor-list").select2({
         placeholder: "Select 3 surveyors"
    });
    $("#vehicle-list").select2({
        placeholder: "Select a vehicle"
    });

    $(function () {
        $('#survey-time').datetimepicker();
    });
    $(function () {
       $('#move-time').datetimepicker();
   });

    var navListItems = $('div.setup-panel div a'),
    allWells = $('.setup-content'),
    allNextBtn = $('.nextBtn');

    allWells.hide();

    navListItems.click(function (e) {
        e.preventDefault();
        var $target = $($(this).attr('href')),
        $item = $(this);

        if (!$item.hasClass('disabled')) {
            navListItems.removeClass('btn-primary').addClass('btn-default');
            $item.addClass('btn-primary');
            allWells.hide();
            $target.show();
            $target.find('input:eq(0)').focus();
        }
    });

    allNextBtn.click(function(){
        var curStep = $(this).closest(".setup-content"),
        curStepBtn = curStep.attr("id"),
        nextStepWizard = $('div.setup-panel div a[href="#' + curStepBtn + '"]').parent().next().children("a"),
        curInputs = curStep.find("input[type='text'],input[type='url']"),
        isValid = true;

        $(".form-group").removeClass("has-error");
        for(var i=0; i<curInputs.length; i++){
            if (!curInputs[i].validity.valid){
                isValid = false;
                $(curInputs[i]).closest(".form-group").addClass("has-error");
            }
        }

        if (isValid)
            nextStepWizard.removeAttr('disabled').trigger('click');
    });

    $('div.setup-panel div a.btn-primary').trigger('click');
    //graph data
    // var data = {
    //     labels: ["January", "February", "March", "April", "May", "June", "July"],
    //     datasets: [
    //     {
    //         label: "My First dataset",
    //         fillColor: "rgba(220,220,220,0.5)",
    //         strokeColor: "rgba(220,220,220,0.8)",
    //         highlightFill: "rgba(220,220,220,0.75)",
    //         highlightStroke: "rgba(220,220,220,1)",
    //         data: [65, 59, 80, 81, 56, 55, 40]
    //     },
    //     {
    //         label: "My Second dataset",
    //         fillColor: "rgba(151,187,205,0.5)",
    //         strokeColor: "rgba(151,187,205,0.8)",
    //         highlightFill: "rgba(151,187,205,0.75)",
    //         highlightStroke: "rgba(151,187,205,1)",
    //         data: [28, 48, 40, 19, 86, 27, 90]
    //     }
    //     ]
    // };
    
    // var ctx = document.getElementById("myChart").getContext("2d");
    // var myBarChart = new Chart(ctx).Bar(data);
});