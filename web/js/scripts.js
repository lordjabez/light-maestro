// @copyright: 2013 Single D Software - All Rights Reserved
// @summary: JavaScript logic for the Light Maestro GUI


'use strict';


// The current page number
var pageNum = 1;

// Store convenience references to navigation buttons. 
var pageChangeLeft;
var pageChangeRight;


// Sends an AJAX command based on scene selection.
function sendCommand() {

    // Calculate the scene identifier.
    var sceneNum = parseInt($(this).html());
    var sceneId = (pageNum - 1) * 24 + (sceneNum - 1);
    
    // Set up the AJAX parameters.
    var url = '/scenes/_current';
    var headers = {'content-type': 'application/json'};
    var data = JSON.stringify({'id': sceneId});
    
    // Send the request. We don't care about the response for now.
    $.ajax({method: 'PUT', url: url, headers: headers, data: data});
    
}


// Updates the page information based on the page number.
function changePage(event) {

    // Swallow the normal event so that the focus outline doesn't show up.
    if (event) {
        event.preventDefault();
    }

    // Update the page number if this function was called due to a button press.
    if (pageChangeLeft.index($(this)) != -1) {
        pageNum = Math.max(1, pageNum - 1);
    }
    else if (pageChangeRight.index($(this)) != -1) {
        pageNum = Math.min(24, pageNum + 1);
    }
    
    // Update the page change button button enable/disable states.
    pageChangeLeft.button(pageNum > 1 ? 'enable' : 'disable');
    pageChangeRight.button(pageNum < 24 ? 'enable' : 'disable');

    // Set the page header according to current page number.
    $('div:jqmData(role="header") h1').text('Page ' + pageNum);
   
}


// Properly resize buttons when the page size changes.
$(window).on('resize', function() {
    $('.ui-btn-inner').css('line-height', '100px');
    var headerHeight = $('div:jqmData(role="header")').outerHeight();
    var footerHeight = $('div:jqmData(role="footer")').outerHeight();
    var targetContentHeight = $(window).outerHeight() - headerHeight - footerHeight;
    var actualContentHeight = $('div:jqmData(role="content")').outerHeight();
    var targetLineHeight = 100 + (targetContentHeight - actualContentHeight) / 4;
    $('.ui-btn-inner').css('line-height', targetLineHeight + 'px');
});


// Executes initialization commands on the page.
$(document).bind('pagebeforeshow', function() {

    // Disable any ability to select text in the GUI
    $('body').bind('selectstart',function() {
        return false;
    });
    
    // Grab references to the page change buttons.
    pageChangeLeft = $('button.page-changer:jqmData(icon="arrow-l")');
    pageChangeRight = $('button.page-changer:jqmData(icon="arrow-r")');

    // Bind command send events to scene select buttons
    $('button.scene-selector').bind('tap', sendCommand);
    
    // Bind page change events to navigation buttons
    $('button.page-changer').bind('tap', changePage);

    // Update the page navigation information
    changePage()
    
});

$(document).bind('pageshow', function() {
    $(window).resize();
});

