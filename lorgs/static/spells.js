/*
    Create all Spell-Elements and their logic
*/


////////////////////////////////////////////////////////////////////////////////
//      GLOBALS
//


////////////////////////////////////////////////////////////////////////////////
//      CREATION
//


/*
// int: which spell are are currently selecting (or null if no selection)
var SELECTED_SPELL = null;
const SELECTED_SPELL_SEPARATOR = "-"

const ALL_CASTS = document.querySelectorAll(".cast");
const CONTAINER = document.querySelector(".player_timelines_container");


function update_selected_spell() {

    var params = new URLSearchParams(location.search);
    var selected_spells = params.get("selected_spells");
    selected_spells = selected_spells ? selected_spells.split(SELECTED_SPELL_SEPARATOR) : [];
    selected_spells = new Set(selected_spells);

    CONTAINER.classList.toggle("selected", selected_spells.size != 0);

    // update all casts
    [...ALL_CASTS].map(cast => {
        cast.classList.toggle("selected", selected_spells.has(cast.dataset.spell_id));
    });
}


// handle spell selection
function select_spell(event) {
    event.stopImmediatePropagation();

    const spell_id = this.dataset.spell_id;

    // Get Args
    var params = new URLSearchParams(location.search);
    var selected_spells = params.get("selected_spells");
    selected_spells = selected_spells ? selected_spells.split(SELECTED_SPELL_SEPARATOR) : [];
    selected_spells = new Set(selected_spells);

    // Update
    const was_selected = selected_spells.has(spell_id);
    if (!event.ctrlKey) { selected_spells.clear();          }
    if (was_selected)   { selected_spells.delete(spell_id); }
    else                { selected_spells.add(spell_id);    }

    // Set
    selected_spells = Array.from(new Set(selected_spells)).sort();
    selected_spells = selected_spells.join(SELECTED_SPELL_SEPARATOR);
    params.set("selected_spells", selected_spells);
    window.history.replaceState({}, '', `${location.pathname}?${params}`);

    update_selected_spell();
}


document.addEventListener('DOMContentLoaded', (event) => {

    ALL_CASTS.forEach(cast => {
        cast.addEventListener("mousedown", select_spell);
    });

    update_selected_spell();
});
*/
