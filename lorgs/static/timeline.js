/* Logic for the Timeline

includes:
    1) movement for the TimelineCursor
    2) timeline scrolling
*/


/*******************************************************************************
                1) TimelineCursor Movement
*******************************************************************************/


const TIMELINE_CURSOR = document.querySelector(".timeline_cursor");
const TIMELINE_CURSOR_HANDLE = document.querySelector(".timeline_cursor_handle");
var cursor_drag_dist = 0, cursor_drag_start_x = 0;

function cursor_drag_start(e) {
    disable_hover_effects();

    e.stopImmediatePropagation();

    TIMELINE_CURSOR.classList.add("active");
    cursor_drag_start_x = e.clientX; // store initial offset

    document.addEventListener("mousemove", cursor_drag_move, {passive: true});
    document.addEventListener("mouseup", cursor_drag_stop, {passive: true, once: true});
}


function cursor_drag_move(e) {
    cursor_drag_dist = cursor_drag_start_x - e.clientX;
    cursor_drag_start_x = e.clientX;
    var x = TIMELINE_CURSOR.offsetLeft - cursor_drag_dist;
    TIMELINE_CURSOR.style.left = x + "px";
    TIMELINE_CURSOR_HANDLE.innerHTML = toMMSS(x / 4);
}


function cursor_drag_stop(e) {
    document.removeEventListener("mousemove", cursor_drag_move);
    document.removeEventListener("mouseup", cursor_drag_stop);
    TIMELINE_CURSOR.classList.remove("active");
    enable_hover_effects();
}

TIMELINE_CURSOR.addEventListener("mousedown", cursor_drag_start, {passive: true});


/*******************************************************************************
                2) Timeline scrolling
*******************************************************************************/

const slider = document.querySelector(".player_timelines_container");
let startX;
let scrollLeft;

function scroll_start(e) {
    disable_hover_effects();

    startX = e.pageX - slider.offsetLeft;
    scrollLeft = slider.scrollLeft;

    document.addEventListener("mousemove", scroll_mousemove, {passive: true});
    document.addEventListener("mouseup", scroll_stop, {passive: true, once: true});
}

function scroll_mousemove(e) {
    const x = e.pageX - slider.offsetLeft;
    const walk = x - startX;
    slider.scrollLeft = scrollLeft - walk;
}

function scroll_stop(e) {
    enable_hover_effects();
    document.removeEventListener("mousemove", scroll_mousemove);
}

slider.addEventListener("mousedown", scroll_start, {passive: true});

// add shift -> side scroll
slider.addEventListener("mousewheel", e => {
    if (!e.shiftKey) return;
    slider.scrollLeft += e.deltaY;
}, {passive: true});
