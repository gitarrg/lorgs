/*
    Create all Spell-Elements and their logic


var SPELLS = {};
{% for s in spells %}
SPELLS[{{s.spell_id}}] = {"g": "{{s.group.class_name_slug}}", "cd": {{s.cooldown}}, "d": {{s.duration}}, "c": "{{s.color or ''}}", "i": "{{s.icon_name}}", "s": {{"true" if s.show else "false"}} }
{% endfor %}
*/


////////////////////////////////////////////////////////////////////////////////
//      GLOBALS
//
const SCALE = 4;
const IMG_ROOT = "https://wow.zamimg.com/images/wow/icons/medium/"


////////////////////////////////////////////////////////////////////////////////
//      CREATION
//

var SPELLS;

// int: which spell are are currently selecting (or null if no selection)
var SELECTED_SPELL = null;

const ALL_CASTS = document.querySelectorAll(".cast");
const CONTAINER = document.querySelector(".player_timelines_container");


// handle spell selection
function select_spell(event) {
    event.stopImmediatePropagation();

    // swap global toggle
    if (SELECTED_SPELL == this.spell_id) {
        // if this spell was selected.. selected None
        SELECTED_SPELL = null;
    } else {
        // if anything else was selected: hightlight this spell
        SELECTED_SPELL = this.spell_id;
    }
    CONTAINER.classList.toggle("selected", SELECTED_SPELL != null);

    // update all casts
    [...ALL_CASTS].map(cast => {
        cast.classList.toggle("selected", SELECTED_SPELL == cast.spell_id);
    });
};


async function create_single_cast(cast) {
    // Get dynamic info from Div
    cast.spell_id = cast.dataset.spell_id;
    const casttime = cast.dataset.casttime

    // Get static info from "DB"
    const spell = SPELLS[cast.spell_id];
    // const cooldown = spell.cooldown * SCALE;
    // const duration = spell.duration * SCALE;
    // const group = spell.group;

    // set initial visibility
    show(cast, spell.show)

    // time when the spell was cast
    cast.style.left = (casttime/1000 * SCALE) + "px";

    if (spell.cooldown > 0) {
        let div = document.createElement("div");
        div.classList.add("cast_cooldown");
        div.style.width = spell.cooldown * SCALE + "px";
        // div.classList.add(`wow-class-bg-${group}`);
        div.style.backgroundColor = spell.color;
        cast.append(div)
    }

    // duration
    if (spell.duration > 0) {
        let div = document.createElement("div");
        div.classList.add("cast_duration");
        // div.classList.add(`wow-class-bg-${group}`);
        div.style.width = spell.duration * SCALE + "px";
        div.style.backgroundColor = spell.color;
        cast.append(div)
    }

    if (spell.icon_name != null) {
        let div = document.createElement("div");
        div.classList.add("cast_icon");
        cast.append(div)

        let img = document.createElement("img");
        img.src = IMG_ROOT + spell.icon_name;
        div.append(img)
    }

    if (casttime > 0) {
        let div = document.createElement("div");
        div.classList.add("cast_text");
        div.innerHTML = toMMSS(casttime / 1000);
        cast.append(div)
    }

    // add click-event
    cast.addEventListener("mousedown", select_spell);
}


function create_all_casts() {
    const tasks = [...ALL_CASTS].map(cast => {create_single_cast(cast)})
    Promise.all(tasks)
}


document.addEventListener('DOMContentLoaded', (event) => {

    console.log("LOAD SPELLS")

    fetch("/api/spells")
        .then(response => response.json())
        .then(data => SPELLS=data)
        .then(create_all_casts)
});

