

function toMMSS(seconds) {
    return new Date(seconds * 1000).toISOString().substr(14, 5);
}


// convert a time "1:23" to seconds
function time_to_seconds(text) {

    const regex = /(?<minutes>\d+):(?<seconds>\d+)/
    const found = text.match(regex)
    if (!found) {return 0}
    return parseInt(found.groups.minutes) * 60 + parseInt(found.groups.seconds)
}


function clamp(num, min, max) {
  return Math.min(Math.max(num, min), max);
}


// show/hide an element (aka jquery.. but js)
function show(element, display=true) {

    if(!element) {return}
    if (display) {
        element.style.display = "block";
    } else {
        element.style.display = "none";
    }
}

function hide(element) {
    show(element, false);
}
