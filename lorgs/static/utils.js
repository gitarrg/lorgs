

// FIXME: why does this take ms?
function toMMSS(seconds) {
    return new Date(seconds * 1000).toISOString().substr(14, 5);
}


// convert a time "1:23" to seconds
function time_to_seconds(text) {

    const regex = /(?<minutes>\d+):(?<seconds>\d{2})/
    const found = text.match(regex)
    if (!found) {return}
    return parseInt(found.groups.minutes) * 60 + parseInt(found.groups.seconds)
}

function seconds_to_time(seconds, {padding=true}) {
    let text = new Date(seconds * 1000).toISOString().substr(14, 5);
    if(!padding && text.charAt(0) === '0') { text = text.substring(1); } // remove leading 0
    return text;
}



// based on: https://stackoverflow.com/a/9461657
function kFormatter(n, digits=2) {

    if (n > 999) {
        return(n/1000).toFixed(digits) + "k"
    }
    return n.toFixed(0);
}



function clamp(num, min, max) {
  return Math.min(Math.max(num, min), max);
}

function randint(min, max) {
  return Math.floor(Math.random() * (max - min) ) + min;
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
