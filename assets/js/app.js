//Bootstrap remember tab
// Javascript to enable link to tab
var hash = document.location.hash;
var prefix = "tab_";
if (hash) {
    $('.nav-tabs a[href='+hash.replace(prefix,"")+']').tab('show');
}

// Change hash for page-reload
$('.nav-tabs a').on('shown', function (e) {
    window.location.hash = e.target.hash.replace("#", "#" + prefix);
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

//custom jquery to trigger dat picker, info pop-over and print category text
$(document).ready(function() {
    $('.datepicker').datepicker();
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
});