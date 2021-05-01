/*
    Create all Spell-Elements and their logic
*/


////////////////////////////////////////////////////////////////////////////////
//      GLOBALS
//

////////////////////////////////////////////////////////////////////////////////
//      CREATION
//

// int: which spell are are currently selecting (or null if no selection)
var SELECTED_SPELL = null;

const ALL_CASTS = document.querySelectorAll(".cast");
const CONTAINER = document.querySelector(".player_timelines_container");


// handle spell selection
function select_spell(event) {
    console.log("select_spell", this.dataset.spell_id)
    event.stopImmediatePropagation();

    // swap global toggle
    if (SELECTED_SPELL == this.dataset.spell_id) {
        // if this spell was selected.. selected None
        SELECTED_SPELL = null;
    } else {
        // if anything else was selected: hightlight this spell
        SELECTED_SPELL = this.dataset.spell_id;
    }
    CONTAINER.classList.toggle("selected", SELECTED_SPELL != null);

    // update all casts
    [...ALL_CASTS].map(cast => {
        cast.classList.toggle("selected", SELECTED_SPELL == cast.dataset.spell_id);
    });
};


document.addEventListener('DOMContentLoaded', (event) => {


    ALL_CASTS.forEach(cast => {
        cast.addEventListener("mousedown", select_spell);
    });
});

/*
*/
