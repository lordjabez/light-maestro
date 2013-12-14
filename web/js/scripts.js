// @copyright: 2013 Single D Software - All Rights Reserved
// @summary: JavaScript logic for the Light Maestro GUI


"use strict";


var JSON_HEADER = {'content-type': 'application/json'}

var pageNum;


function sendCommand(event) {
    var sceneNum = parseInt($(this).html());
    var sceneId = (pageNum - 1) * 24 + (sceneNum - 1);
    var url = '/scenes/_current';
    var data = JSON.stringify({'id': sceneId});
    $.ajax({ url: url, method: 'PUT', headers: JSON_HEADER, data: data});
}


$(document).on("pagebeforeshow", function(event, data) {

    // Disable any ability to select text in the GUI
    $('body').bind('selectstart',function() {
        return false;
    });

    // Grab the page identifier from the URL.
    pageNum = parseInt(location.search.split('=')[1]);

    // Set the page header according to the document title and optional id.
    var header = document.title;
    if (pageNum) {
        header += ' ' + pageNum;
    }
    $('div:jqmData(role="header") h1').text(header);

    // TODO do we need to figure out which page we're on here?
    $('button.scene-selector').bind('tap', sendCommand);

});
