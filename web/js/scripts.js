// @copyright: 2013 Single D Software - All Rights Reserved
// @summary: JavaScript logic for the Light Maestro GUI


'use strict'


var JSON_HEADER = {'content-type': 'application/json'}


var status = {}
var channels = {}
var scenes = []

var sceneid = null
var scene = null


function areDifferent(obj1, obj2){
  return JSON.stringify(obj1) !== JSON.stringify(obj2);
}

function toHex(n) {
    var prefix = n < 16 ? '0' : ''
    return prefix + n.toString(16)
}

function getNum(elem) {
    if (elem === undefined) return
    var id = elem.attr('id')
    if (id === undefined) return
    return parseInt(id.split('-')[1]) * 4 - 3
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
    for (var f = 1; f <= 24; f++) {
        var a = channels[f * 4 - 3]
        var r = channels[f * 4 - 2]
        var g = channels[f * 4 - 1]
        var b = channels[f * 4 - 0]
        if ($.inArray(f, [1, 3, 4, 6, 8, 9, 11, 13, 15, 16]) != -1) {
            var color = getWhite(a, r, g)
        }
        else {
            var color = getColor(a, r, g, b, 0.33)
        }
        var id = 'fixture-' + f.toString()
        $('label[for="' + id + '"] .ui-btn-inner').css('background', color)
    }

}

function pollData() {
    $.ajax({method: 'GET', url: '/data', success: setData, error: alertNoComm})
}

function refreshChannels(data) {
    channels = data.channels
    colorFixtures()
}

function refreshScenes(data) {
    scenes = data.scenes
    var html = ''
    for (var s = 0; s < scenes.length; s++) {
        var highlight = scenes[s] == data.status.scene ? 'class=" ui-btn-active"' : ''
        html += '<li data-icon="false"' + highlight + '><a>' + data.scenes[s] + '</a></li>'
    }
    $('#scene-list').html(html).listview('refresh')
    $('#scene-list a').unbind().bind('click', changeScene)
}

function setData(data) {
    if (data.status.condition != 'operational') {
        alertNonOp(data.status.interface)
    }
    else {
        hideAlert()
    }
    if (areDifferent(channels, data.channels)) {
        refreshChannels(data)
    }
    if (areDifferent(scenes, data.scenes)) {
        refreshScenes(data)
    }
    if (data.status.scene) {
        if (data.status.scene != sceneid) {
            sceneid = data.status.scene
            refreshScenes(data)
            $.ajax({method: 'GET', url: '/scenes/' + sceneid, success: setScene, error: alertNoComm})
        }
    }
}

function setScene(data) {
    scene = data
}

function refreshSliders() {
    var fixture = $(this).prop('checked') ? $(this) : $('#fixture-layout input:checked').first()
    var num = getNum(fixture)
    var whitesChecked = $('#fixture-layout input.fixture-white:checked').length > 0
    var colorsChecked = $('#fixture-layout input.fixture-color:checked').length > 0
    if (whitesChecked) {
        if (colorsChecked) {
            setSlidersMixed(num)
        }
        else {
            setSlidersWhites(num)
        }
    }
    else {
        if (colorsChecked) {
            setSlidersColors(num)
        }
        else {
            setSlidersNone()
        }
    }
}

function setSliderValues(a, r, g, b) {
    $('#value-alpha').val(a || 0).slider('refresh')
    $('#value-red').val(r || 0).slider('refresh')
    $('#value-green').val(g || 0).slider('refresh')
    $('#value-blue').val(b || 0).slider('refresh')
}

function setSliderLabels(a, r, g, b) {
    $('label[for="value-alpha"]').html(a || '')
    $('label[for="value-red"]').html(r || '')
    $('label[for="value-green"]').html(g || '')
    $('label[for="value-blue"]').html(b || '')
}

var sliderMode = 'none'

function setSlidersNone() {
    sliderMode = 'none'
    setSliderValues()
    setSliderLabels()
    $('#white-palette').hide()
    $('#color-palette').hide()
    $('#value-sliders input').slider('disable')
}

function setSlidersWhites(num) {
    sliderMode = 'white'
    setSliderValues(channels[num+0], channels[num+1], channels[num+2])
    setSliderLabels('Brightness', 'Warm', 'Cool')
    $('#white-palette').show()
    $('#color-palette').hide()
    $('#value-sliders input').slider('enable')
    $('#value-blue').slider('disable')
}

function setSlidersColors(num) {
    sliderMode = 'color'
    setSliderValues(channels[num+0], channels[num+1], channels[num+2], channels[num+3])
    setSliderLabels('Brightness', 'Red', 'Green', 'Blue')
    $('#white-palette').hide()
    $('#color-palette').show()
    $('#value-sliders input').slider('enable')
}

function setSlidersMixed(num) {
    sliderMode = 'mixed'
    setSliderValues(channels[num+0])
    setSliderLabels('Brightness')
    $('#white-palette').hide()
    $('#color-palette').hide()
    $('#value-sliders input').slider('disable')
    $('#value-alpha').slider('enable')
}

function selectFixtures() {
    var type = $(this).html()
    var whitesChecked = type == 'All' || type == 'Whites'
    var colorsChecked = type == 'All' || type == 'Colors'
    $('input[class="fixture-white"]').prop('checked', whitesChecked)
    $('input[class="fixture-color"]').prop('checked', colorsChecked)
    $('#fixture-layout input').checkboxradio('refresh')
    refreshSliders()
}

var sliding = false

function startSlide() {
    sliding = true
}

function stopSlide() {
    sliding = false
}

function setSlidersBackground(color) {
    var a = parseInt($('#value-alpha').val())
    var r = parseInt($('#value-red').val())
    var g = parseInt($('#value-green').val())
    var b = parseInt($('#value-blue').val())
    switch (sliderMode) {
        case 'none':
            var color = '#000000'
            break
        case 'white':
            var color = getWhite(a, r, g)
            break
        case 'color':
            var color = getColor(a, r, g, b, 0.33)
            break
        case 'mixed':
            var hex = toHex(Math.round(Math.pow(a / 100.0, 0.5) * 255))
            var color = '#' + hex + hex + hex
            break
    }
    $('.ui-slider-bg').css('background', color)
    /*var aHex = toHex(Math.round(Math.pow(a / 100.0, 0.5) * 255))
    $('#value-alpha + div .ui-slider-bg').css('background', '#' + aHex + aHex + aHex)
    if (sliderMode != 'white') {
        $('#value-red + div .ui-slider-bg').css('background', getColor(100.0, r, 0.0, 0.0, 0.33))
    }
    else {
        $('#value-red + div .ui-slider-bg').css('background', getWhite(100.0, r, 0.0))
    }
    if (sliderMode != 'white') {
        $('#value-green + div .ui-slider-bg').css('background', getColor(100.0, 0.0, g, 0.0, 0.33))
    }
    else {
        $('#value-green + div .ui-slider-bg').css('background', getWhite(100.0, 0.0, g))
    }
    $('#value-blue + div .ui-slider-bg').css('background', getColor(100.0, 0.0, 0.0, b, 0.33))*/
}

function changeValues(event) {
    setSlidersBackground()
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
    var newChannels = {}
    $('#fixture-layout input:checked').each( function() {
        var num = getNum($(this))
        newChannels[num + offset] = value
    })
    var data = JSON.stringify({'channels': newChannels})
    $.ajax({method: 'POST', url: '/channels/_load', headers: JSON_HEADER, data: data, success: pollData})
}

function pickColor() {
    var components = $(this).attr('color').split(',').map(parseFloat)
    setSliderValues(components[0], components[1], components[2], components[3])
    var newChannels = {}
    $('#fixture-layout input:checked').each( function() {
        var num = getNum($(this))
        for (var c = 0; c < components.length; c++) {
            newChannels[num + c] = components[c]
        }
    })
    var data = JSON.stringify({'channels': newChannels})
    $.ajax({method: 'POST', url: '/channels/_load', headers: JSON_HEADER, data: data, success: pollData})
}

function saveScene(event) {
    $.mobile.loading('show')
    var sceneid = $('#scene-name').val()
    var fade = parseInt($('#scene-fade').val())
    var url = '/scenes/' + sceneid
    var data = JSON.stringify({'channels': channels, 'fade': fade})
    $.ajax({method: 'PUT', url: url, headers: JSON_HEADER, data: data, success: saveSuccess, error: saveError, complete: saveComplete})
}

function saveSuccess() {
    pollData()
    $.mobile.loading('hide')
    $('.ui-dialog').dialog('close')
}

function saveError() {
    $('div[data-id="save-status-footer"]').show().html('<h3>Save Failed</h3>')
}

function saveComplete() {
    $.mobile.loading('hide')
}

function changeScene(event) {
    var sceneid = $(this).html()
    $.ajax({method: 'POST', url: '/scenes/' + sceneid + '/_change', success: pollData})
}

function alertNoComm() {
    displayAlert('User Interface not communicating with Light Maestro')
}

function alertNonOp(device) {
    displayAlert('Light Maestro not communicating with ' + device)
}

function displayAlert(text) {
    $('div[data-id="status-footer"]').html('<h3>' + text + '</h3>').show()
}

function hideAlert() {
    $('div[data-id="status-footer"]').hide()
}

// Things to do before the page is shown.
$(document).bind('pagebeforeshow', function() {

    // Disable any ability to select text in the GUI.
    $('body').unbind().bind('selectstart', function() {
        return false
    })

    // Bind a handler to each fixture click.
    $('#fixture-layout input').unbind().bind('click', refreshSliders)

    // Bind the select fixture functions to selection buttons.
    $('#fixture-selectors button').unbind().bind('click', selectFixtures)

    // Bind the change value function to the sliders.
    $('#value-sliders input').unbind()
    $('#value-sliders input').bind('slidestart', startSlide)
    $('#value-sliders input').bind('change', changeValues)
    $('#value-sliders input').bind('slidestop', stopSlide)

    // Build the palettes and bind handlers to them.
    $('#white-palette button').each( function() {
        var components = $(this).attr('color').split(',').map(parseFloat)
        $(this).parent().css('background', getWhite(components[0], components[1], components[2]))
        $(this).html('&nbsp;&nbsp;&nbsp;&nbsp;').button('refresh')
    })
    $('#color-palette button').each( function() {
        var components = $(this).attr('color').split(',').map(parseFloat)
        $(this).parent().css('background', getColor(components[0], components[1], components[2], components[3], 0.33))
        $(this).html('&nbsp;&nbsp;&nbsp;&nbsp;').button('refresh')
    })
    $('#white-palette button').unbind().bind('click', pickColor)
    $('#color-palette button').unbind().bind('click', pickColor)

    // Bind the scene saving function
    $('#scene-save').unbind().bind('click', saveScene)

    // Grab current scene data to populate dialog
    if (sceneid) {
        $('#scene-name').val(sceneid)
    }
    if (scene) {
        $('#scene-fade').val(scene.fade)
    }

    // Update sliders
    refreshSliders()

    // Hide any status footers (they'll be auto-redisplayed if needed)
    $('div[data-role="footer"]').hide()

})

// Run the poller at the given rate.
setInterval(pollData, 500)
