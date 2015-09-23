//Bootstrap remember tab
// Javascript to enable link to tab
$(function() {
     // Javascript to enable link to tab
    var hash = document.location.hash;
    if (hash) {
    console.log(hash);
    $('.nav-tabs a[href='+hash+']').tab('show');
    }

    // Change hash for page-reload
    $('a[data-toggle="tab"]').on('show.bs.tab', function (e) {
    window.location.hash = e.target.hash;
    });
});

//
function submitClose(){
    opener.location.reload(true);
    self.close();
}

//App specific JavaScript//App specific JavaScript
$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

//custom jquery to trigger date picker, info pop-over and print category text
$(document).ready(function() {


    //Check for chrome and don't provide a datetime pickers for it
    var browser = navigator.userAgent;

    if(browser.indexOf("Chrome") < 0){
       $('.datepicker').datepicker({dateFormat: "yy-mm-dd"});
    }
});


$('input[type="file"]').each(function() {
    var $file = $(this), $form = $file.closest('.upload-form');
    $file.ajaxSubmitInput({
        url: '/incident/add/', //URL where you want to post the form
        beforeSubmit: function($input) {
            //manipulate the form before posting
        },
        onComplete: function($input, iframeContent, options) {
            if (iframeContent) {
                $input.closest('form')[0].reset();
                if (!iframeContent) {
                    return;
                }
                var iframeJSON;
                try {
                    iframeJSON = $.parseJSON(iframeContent);
                    //use the response data
                } catch(err) {
                    console.log(err)
                }
            }
        }
    });
});


$(document).ready(function() {
    /*
     * Handle change in the province drop-down; updates the distirct drop-down accordingly.
     */
    $("select#id_province").change(function() {
        var selected_province = $(this).val();
        if (selected_province == undefined || selected_province == -1 || selected_province == '') {
            $("select#id_district").html("<option>--Province--</option>");
        } else {
            var url = "/activitydb/province/" + selected_province + "/province_json/";
            $.getJSON(url, function(district) {
                var options = '<option value="0">--District--</option>';
                for (var i = 0; i < district.length; i++) {
                    options += '<option value="' + district[i].pk + '">' + district[i].fields['name'] + '</option>';
                }

                $("select#id_district").html(options);
                $("select#id_district option:first").attr('selected', 'selected');
            });
        }

        // page-specific-action call if a page has implemented the 'country_dropdwon_has_changed' function
        if(typeof country_dropdwon_has_changed != 'undefined') country_dropdwon_has_changed(selected_country);
    });

    /*
     * Handle change in office drop-down
     */
    $("select#id_district").change(function(vent) {
        var selected_distirct = $(this).val();
        if (selected_distirct == -1) {
            return;
        }

        // page-specific-action call if a page has implemented the 'office_dropdown_has_changed' function
        if(typeof district_dropdown_has_changed != 'undefined') distirct_dropdown_has_changed(district_office);
    });

    /*
     * UPDATE BUDGET TOTAL
    */
    function updateBudget()
    {
        var mc_budget = parseFloat($("#mc_budget").val());
        var other_bidget = parseFloat($("#other_budget").val());
        var total = mc_budget + other_budget;
        var total = total.toFixed(2);
        $("#total_budget").val(total);
    }
    $(document).on("change, keyup", "#mc_budget", updateBudget);
    $(document).on("change, keyup", "#other_budget", updateBudget);

    /*
     * Calculate Total Indirect Beneficiaries
    */
    function updateBens()
    {
        var direct_bens = parseFloat($("#id_estimated_num_direct_beneficiaries").val());
        var avg_houshold_size = parseFloat($("#id_average_household_size").val());
        var total = direct_bens * avg_houshold_size;
        var total = total.toFixed(2);
        $("#id_estimated_num_indirect_beneficiaries").val(total);
    }
    $(document).on("change, keyup", "#id_estimated_num_direct_beneficiaries", updateBens);
    $(document).on("change, keyup", "#id_average_household_size", updateBens);

    /*
     * Trained TOTAL
    */
    function updateTrained()
    {
        var male = parseFloat($("#id_estimate_male_trained").val());
        var female = parseFloat($("#id_estimate_female_trained").val());
        var total = male + female;
        var total = total.toFixed(0);
        $("#id_estimate_total_trained").val(total);
    }
    $(document).on("change, keyup", "#id_estimate_male_trained", updateTrained);
    $(document).on("change, keyup", "#id_estimate_female_trained", updateTrained);

    /*
     * CFW Workers TOTAL
    */
    function updateCFW()
    {
        var male = parseFloat($("#id_cfw_estimate_male").val());
        var female = parseFloat($("#id_cfw_estimate_female").val());
        var total = male + female;
        var total = total.toFixed(0);
        $("#id_cfw_estimate_total").val(total);
    }
    $(document).on("change, keyup", "#id_cfw_estimate_male", updateCFW);
    $(document).on("change, keyup", "#id_cfw_estimate_female", updateCFW);

    $('.dropdown-menu a').on('click', function(){
        $(this).parent().parent().prev().html($(this).html() + '<span class="caret"></span>');
    })
});

