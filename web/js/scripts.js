// @copyright: 2013 Single D Software - All Rights Reserved
// @summary: JavaScript logic for the Light Maestro GUI


'use strict';


// Sends an AJAX command based on scene selection.
function sendCommand() {

    // Pull the scene identifier from the button label.
    var sceneId = parseInt($(this).html());

    // Send the request. We don't care about the response for now.
    $.ajax({method: 'POST', url: '/scenes/' + sceneId + '/_load'});

}


// Properly resize buttons when the page size changes.
$(window).on('resize', function() {
    $('.ui-btn-inner').css('line-height', '100px');
    var headerHeight = $('div:jqmData(role="header")').outerHeight();
    var footerHeight = $('div:jqmData(role="footer")').outerHeight();
    var targetContentHeight = $(window).outerHeight() - headerHeight - footerHeight;
    var actualContentHeight = $('div:jqmData(role="content")').outerHeight();
    var targetLineHeight = 100 + (targetContentHeight - actualContentHeight) / 3;
    $('.ui-btn-inner').css('line-height', targetLineHeight + 'px');
});


// Executes initialization commands on the page.
$(document).bind('pagebeforeshow', function() {

    // Disable any ability to select text in the GUI
    $('body').bind('selectstart',function() {
        return false;
    });

    // Bind command send events to scene select buttons
    $('button.scene-selector').bind('tap', sendCommand);

});


$(document).bind('pageshow', function() {
    $(window).resize();
});
