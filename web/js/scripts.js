// @copyright: 2013 Single D Software - All Rights Reserved
// @summary: JavaScript logic for the Light Maestro GUI


'use strict';


// TODO comments
// TODO read channel values when picking individual fixture
// TODO arrange banks
// TODO add "select all in bank" button? perhaps with double tap or long-press?

function selectFixtures() {
    var type = $(this).html();
    var whitesChecked = type == 'All' || type == 'Whites';
    var colorsChecked = type == 'All' || type == 'Colors';
    $('input[class="fixture-white"]').prop('checked', whitesChecked);
    $('input[class="fixture-color"]').prop('checked', colorsChecked);
    $('input[type="checkbox"]').checkboxradio('refresh');
}

function changeValues(event) {
    var alpha = parseFloat($('#value-alpha').val());
    var red = parseFloat($('#value-red').val());
    var green = parseFloat($('#value-green').val());
    var blue = parseFloat($('#value-blue').val());
    var channels = {}
    $('input[type="checkbox"]').each( function() {
        if($(this).prop('checked')) {
           var id = parseInt($(this).attr('id').split('-')[1]);
           channels[id + 0] = alpha;
           channels[id + 1] = red;
           channels[id + 2] = green;
           channels[id + 3] = blue;
       }
    });
    $.ajax({data: JSON.stringify({'channels': channels})});
}

// Things to do before the page is shown.
$(document).bind('pagebeforeshow', function() {

    // Set up AJAX calls.
    $.ajaxSetup({method: 'POST', url: '/channels/_load', headers: {'content-type': 'application/json'}});

    // Disable any ability to select text in the GUI.
    $('body').bind('selectstart',function() {
        return false;
    });

    // Bind the select fixture function to selection buttons.
    $('button').bind('tap', selectFixtures);

    // Bind the change value function to the sliders (TODO make this one call).    
    $('#value-alpha').bind('change', changeValues);
    $('#value-red').bind('change', changeValues);
    $('#value-green').bind('change', changeValues);
    $('#value-blue').bind('change', changeValues);

});

