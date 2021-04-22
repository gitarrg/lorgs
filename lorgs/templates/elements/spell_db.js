/*
    Create all Spell-Elements and their logic
*/


var SPELLS = {};
{% for s in wow_data.SPELLS.values() %}
SPELLS[{{s.spell_id}}] = {"g": "{{s.group.class_name_slug}}", "cd": {{s.cooldown}}, "d": {{s.duration}}, "c": "{{s.color or ''}}", "i": "{{s.icon}}"}
{% endfor %}


////////////////////////////////////////////////////////////////////////////////
//      GLOBALS
//
const SCALE = 4;
const IMG_ROOT = "https://wow.zamimg.com/images/wow/icons/medium/"


////////////////////////////////////////////////////////////////////////////////
//      CREATION
//


// int: which spell are are currently selecting (or null if no selection)
var SELECTED_SPELL = null;

const ALL_CASTS = document.querySelectorAll(".cast");
const CONTAINER = document.querySelector(".player_timelines_container");


// handle spell selection
function select_spell() {

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
    ALL_CASTS.forEach(cast => {
        cast.classList.toggle("selected", SELECTED_SPELL == cast.spell_id);
    });
};


function create_single_cast(cast) {
    // Get dynamic info from Div
    cast.spell_id = $(cast).attr("data-spell_id");

    // Get static info from "DB"
    const spell_data = SPELLS[cast.spell_id];
    const cooldown = spell_data.cd * SCALE;
    const duration = spell_data.d * SCALE;
    const color = spell_data.c;
    const icon = spell_data.i;
    const group = spell_data.g;

    // time when the spell was cast
    const casttime = $(cast).attr("data-cast-time");
    cast.style.left = (casttime/1000 * SCALE) + "px";

    if (cooldown > 0) {
        let div = document.createElement("div");
        div.classList.add("cast_cooldown");
        div.style.width = cooldown + "px";
        div.classList.add(`wow-class-bg-${group}`);
        div.style.backgroundColor = color;
        cast.append(div)
    }

    // duration
    if (duration > 0) {
        let div = document.createElement("div");
        div.classList.add("cast_duration");
        div.classList.add(`wow-class-bg-${group}`);
        div.style.width = duration + "px";
        div.style.backgroundColor = color;
        cast.append(div)
    }

    if (icon != null) {
        let div = document.createElement("div");
        div.classList.add("cast_icon");
        cast.append(div)

        let img = document.createElement("img");
        img.src = IMG_ROOT + icon;
        div.append(img)
    }

    if (casttime > 0) {
        let div = document.createElement("div");
        div.classList.add("cast_text");
        div.innerHTML = toMMSS(casttime / 1000);
        cast.append(div)
    }
}



$( document ).ready(function(){

    ALL_CASTS.forEach(cast => {
        create_single_cast(cast)
        cast.onclick = select_spell;
    });
});



