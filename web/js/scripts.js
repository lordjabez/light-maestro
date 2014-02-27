// @copyright: 2013 Single D Software - All Rights Reserved
// @summary: JavaScript logic for the Light Maestro GUI


'use strict'


var JSON_HEADER = {'content-type': 'application/json'}


var channels = {}

function toHex(n) {
    var prefix = n < 16 ? '0' : ''
    return prefix + n.toString(16)
}

function getColor(a, r, g, b, factor) {
    var alpha = Math.pow(a / 100.0, 0.5)
    var red = Math.round(Math.pow(r * alpha / 100.0, factor) * 255.0)
    var green = Math.round(Math.pow(g * alpha / 100.0, factor) * 255.0)
    var blue = Math.round(Math.pow(b * alpha / 100.0, factor) * 255.0)
    return '#' + toHex(red) + toHex(green) + toHex(blue)
}

function getWhite(a, y, b) {
    var alpha = a / 100.0 * Math.max(y, b)
    var red = 100.0
    var green = 100.0
    var blue = 100.0
    if (y > b) {
        blue -= (y - b) / 2.0
    }
    else {
        red -= (b - y) / 2.0
    }
    return getColor(alpha, red, green, blue, 1.0)
}

function colorFixtures() {
    for(var f = 1; f <= 24; f++) {
        var a = channels[f * 4 - 3]
        var r = channels[f * 4 - 2]
        var g = channels[f * 4 - 1]
        var b = channels[f * 4 - 0]
        if($.inArray(f, [1, 3, 4, 6, 8, 9, 11, 13, 15, 16]) != -1) {
            var color = getWhite(a, r, g)
        }
        else {
            var color = getColor(a, r, g, b, 0.25)
        }
        var id = 'fixture-' + f.toString()
        $('label[for="' + id + '"] .ui-btn-inner').css('background', color)
    }
}

function pollChannels() {
    $.ajax({method: 'GET', url: '/channels', success: setChannels})
}

function setChannels(data) {
    channels = data['channels']
    colorFixtures()
}

function selectFixture() {
    if($(this).prop('checked')) {
        var id = parseInt($(this).attr('id').split('-')[1]) * 4 - 3
        $('#value-alpha').val(channels[id + 0]).slider('refresh')
        $('#value-red').val(channels[id + 1]).slider('refresh')
        $('#value-green').val(channels[id + 2]).slider('refresh')
        $('#value-blue').val(channels[id + 3]).slider('refresh')
    }
}

function selectFixtures() {
    var type = $(this).html()
    var whitesChecked = type == 'All' || type == 'Whites'
    var colorsChecked = type == 'All' || type == 'Colors'
    $('input[class="fixture-white"]').prop('checked', whitesChecked)
    $('input[class="fixture-color"]').prop('checked', colorsChecked)
    $('input[type="checkbox"]').checkboxradio('refresh')
    $('.fixture-layout input[type="checkbox"]').each( function() {
        if($(this).prop('checked')) {
            var id = parseInt($(this).attr('id').split('-')[1]) * 4 - 3
            $('#value-alpha').val(channels[id + 0]).slider('refresh')
            $('#value-red').val(channels[id + 1]).slider('refresh')
            $('#value-green').val(channels[id + 2]).slider('refresh')
            $('#value-blue').val(channels[id + 3]).slider('refresh')
        }
    });
}

var sliding = false

function changeValues(event) {
    if (!sliding) {
        return
    }
    var channel = event.target.id
    switch (channel) {
        case 'value-alpha': var offset = 0; break
        case 'value-red': var offset = 1; break
        case 'value-green': var offset = 2; break
        case 'value-blue': var offset = 3; break
    }
    var value = parseFloat($('#' + channel).val())
    $('.fixture-layout input[type="checkbox"]').each( function() {
        if($(this).prop('checked')) {
           var id = parseInt($(this).attr('id').split('-')[1]) * 4 - 3
           channels[id + offset] = value
       }
    });
    var data = JSON.stringify({'channels': channels})
    $.ajax({method: 'POST', url: '/channels/_load', headers: JSON_HEADER, data: data})
}

function controlScene(event) {
    var command = event.target.id
    var sceneid = $('#scene-name').val()
    var fade = parseInt($('#scene-fade').val())
    var url = '/scenes/' + sceneid
    var data = JSON.stringify({'channels': channels, 'fade': fade})
    switch(command) {
        case 'scene-save': $.ajax({method: 'PUT', url: url, headers: JSON_HEADER, data: data}); break
        case 'scene-load': $.ajax({method: 'POST', url: url + '/_load'}); break
        case 'scene-change': $.ajax({method: 'POST', url: url + '/_change'}); break
    }
}

// Things to do before the page is shown.
$(document).bind('pagebeforeshow', function() {

    // Disable any ability to select text in the GUI.
    $('body').bind('selectstart', function() {
        return false
    });

    // Bind a handler to each fixture click.
    $('input[type=checkbox]').bind('click', selectFixture)

    // Bind the select fixture functions to selection buttons.
    $('.fixture-selectors button').bind('click', selectFixtures)

    // Bind the save/load/change scene buttons.
    $('.scene-controls button').bind('click', controlScene)

    // Bind the change value function to the sliders.
    $('.value-sliders').bind('slidestart', function() { sliding = true })
    $('.value-sliders').bind('change', changeValues)
    $('.value-sliders').bind('slidestop', function() { sliding = false })

    // Set up channel poller.
    setInterval(pollChannels, 250)

});

