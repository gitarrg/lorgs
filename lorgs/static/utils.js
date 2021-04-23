
function toMMSS(sec_num) {
    // var sec_num = parseInt(this, 10); // don't forget the second param
    var minutes = Math.floor((sec_num) / 60);
    var seconds = Math.floor(sec_num) - (minutes * 60);

    if (minutes < 10) {minutes = "0"+minutes;}
    if (seconds < 10) {seconds = "0"+seconds;}
    return minutes+':'+seconds;
}


// show/hide an element (aka jquery.. but js)
function show(element, display=true) {
    if (display) {
        element.style.display = "block";
    } else {
        element.style.display = "none";
    }
}

function hide(element) {
    show(element, false);
}

