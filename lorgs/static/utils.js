

function toMMSS(seconds) {
    return new Date(seconds * 1000).toISOString().substr(14, 5);
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
