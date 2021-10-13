
import { createSlice } from '@reduxjs/toolkit'
import { createSelector } from 'reselect'


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

export function get_filters(state) {
    return state.ui.filters
}

export function get_filter_value(state, attr_name) {
    return state.ui.filters[attr_name]
}


export const get_is_loading = createSelector(
    (state) => state.ui._loading, // dependency
    (loading_state) => {
        return Object.values(loading_state).some(v => v == true)
    }
)


export function get_tooltip(state) {
    return state.ui.tooltip
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

        _loading: {}, // elements that are loading

        spec_slug: undefined, // currently selected spec
        boss_slug: undefined, // currently selected boss

        // Timeline Options
        settings: {
            show_casticon: true,
            show_casttime: true,
            show_duration: true,
            show_cooldown: true,
        },

        // fight/player filter settings
        filters: {

            // player filters
            role: {},
            class: { boss: false },  // for now, bosses are hidden by default (except the pinned ones)
            spec: {},
            covenant: {},

            // fight filters
            killtime: {min: undefined, max: undefined},
        },

        tooltip: {
            content: "",
            position: {x: 0, y: 0}
        }
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

        update_settings: (state, action) => {
            state.settings = {...state.settings, ...action.payload}
            return state
        },

        // Filters
        set_filter: (state, action) => {
            const { group, name, value } = action.payload
            state.filters[group] = state.filters[group] || {}
            state.filters[group][name] = value
            // state.filters = {...state.filters, ...action.payload}
            return state
        },

        set_filters: (state, action) => {
            state.filters = {...state.filters, ...action.payload}
            return state
        },

        // loading
        set_loading: (state, {key, value}) => {
            state._loading[key] = value
            return state
        },

        set_mode: (state, action) => {
            state.mode = action.payload
            return state
        },

        set_tooltip: (state, action) => {
            const {content, position } = action.payload
            state.tooltip.content = content
            state.tooltip.position = position
            return state
        }
    },
})


export const {
    set_boss,
    set_filter,
    set_filters,
    set_mode,
    set_spec,
    set_tooltip,
    set_value,
    set_values,
    update_settings,
} = SLICE.actions


export default SLICE.reducer
