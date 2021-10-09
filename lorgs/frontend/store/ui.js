
import { createSlice } from '@reduxjs/toolkit'


// modes to switch some page related features
export const MODES = {
    NONE: "none",
    SPEC_RANKING: "spec_ranking",
    COMP_RANKING: "comp_ranking",
}


////////////////////////////////////////////////////////////////////////////////
// Actions
//
export function get_mode(state) {
    return state.ui.mode
}

export function get_value(state, attr_name) {
    return state.ui[attr_name]
}


/* add a prefix to the input, to aid with sorting */
function _sort_spell_type_sort_key(spell_type) {

    let prefix = "50" // start middle
    if (spell_type == "raid")           { prefix = "60"} // raid cd's after class
    if (spell_type.startsWith("other")) { prefix = "80"} // other types go behind

    return [prefix, spell_type].join("-")
}

/* Sort spell types as:
   - boss
   - specs
   - other
*/
export function sort_spell_types(spell_types) {
    return spell_types.sort((a, b) => {
        const key_a = _sort_spell_type_sort_key(a)
        const key_b = _sort_spell_type_sort_key(b)
        return key_a > key_b ? 1 : -1
    })
}


////////////////////////////////////////////////////////////////////////////////
// Slice
//

const SLICE = createSlice({
    name: "ui",

    initialState: {
        mode: MODES.NONE,
        is_loading: true,

        spec_slug: undefined, // currently selected spec
        boss_slug: undefined, // currently selected boss

        // Timeline Options
        show_casticon: true,
        show_casttime: true,
        show_duration: true,
        show_cooldown: true,
    },

    reducers: {

        // dont hate on me
        set_value: (state, action) => {
            state[action.payload.field] = action.payload.value
            return state;
        },

        set_values: (state, action) => {
            return { ...state, ...action.payload}
        },

        set_mode: (state, action) => {
            state.mode = action.payload
            return state
        },
    },
})


export const {
    set_value,
    set_values,
    set_mode,
    set_boss,
    set_spec,

} = SLICE.actions


export default SLICE.reducer