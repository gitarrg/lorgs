
import { createSlice } from '@reduxjs/toolkit'
import { createSelector } from 'reselect'

import API from '../api.js'
import { set_fights } from './fights.js'


const ICON_ROOT = "https://wow.zamimg.com/images/wow/icons/small"



////////////////////////////////////////////////////////////////////////////////
// Actions
//

export function get_spell(state, spell_id) {
    return state.spells.all_spells[spell_id] || {}
}


export function get_spells(state, spell_ids=[]) {
    return state.spells.all_spells
}

/*
    Note: returns a new list each time. useMemo this one!
*/

export const get_spells_by_type = createSelector(
    get_spells,
    (spells) => {
        const v = {}
        Object.values(spells).forEach(spell => {
            v[spell.spell_type] = v[spell.spell_type] || []
            v[spell.spell_type].push(spell)

        })
        return v
    }
)


export function get_spell_visible(state, spell_id) {
    // undefined is considered true in this case
    return state.spells.spell_display[spell_id] !== false;
}

/* check if a given spell was ever used.
   Used to eg.: avoid creating spell buttons for ever possible trinket,
   even if nobody is using it.
*/
export function get_used_spells(state) {
    return state.spells.used_spell_ids
}


export function filter_used_spells(spells, fights) {

    if (!spells) { return {} }
    if (!fights) { return {} }

    let used_spells = new Set()
    fights.forEach(fight => {


        if (fight.boss && fight.boss.casts) {
            fight.boss.casts.forEach(cast => {
                used_spells.add(cast.id)
            })
        }

        (fight.players || []).forEach(player => {
            (player.casts || []).forEach(cast => {
                used_spells.add(cast.id)
            })
        })
    })
    return Array.from(used_spells) // Set to Array
}


// add the image and img path
export function process_spells(spells = {}) {
    Object.values(spells).forEach(spell => {
        spell.specs = spell.specs || []
        spell.icon = spell.icon || "" // check mostly due to the loading data
        spell.icon_path = spell.icon.startsWith("/") ? spell.icon : `${ICON_ROOT}/${spell.icon}`
    })
    return spells;
}



////////////////////////////////////////////////////////////////////////////////
// Slice
//

const SLICE = createSlice({
    name: "spells",

    initialState: {

        // dict[int: dict]: all spells
        all_spells: {},

        // list[int]: id's of all spells that have been used
        used_spell_ids: [],

        // dict[spell_id: bool]: toggle for visible spells
        spell_display: {},

        // list[int]: all spells that are currently selected/focused
        selected_spells: [],

    },

    reducers: {

        set_spells: (state, action) => {
            state.all_spells = action.payload
            state.all_spells = process_spells(state.all_spells)

            Object.values(state.all_spells).forEach(spell => {
                state.spell_display[spell.spell_id] = spell.show;
            })

            return state
        },

        update_used_spells: (state, action) => {
            const {spells, fights} = action.payload
            state.used_spell_ids = filter_used_spells(spells, fights)
            state.used_spell_ids = Array.from(state.used_spell_ids) // Set to Array
            return state
        },

        set_spell_visible: (state, action) => {
            const { spell_id, visible } = action.payload
            state.spell_display[spell_id] = visible
            return state;
        },

        spell_selected: (state, action) => {
            const { spell_id, selected, deselect_others } = action.payload

            let selected_spells = new Set(state.selected_spells)

            if (deselect_others) {
                selected_spells.clear()
            }

            if (selected) {
                selected_spells.add(spell_id)
            } else {
                selected_spells.delete(spell_id)
            }

            state.selected_spells = Array.from(selected_spells)
            return state
        }
    }, // reducers

    extraReducers: (builder) => {

        builder

        .addCase(set_fights, (state, action) => {
            const fights = action.payload

            state.used_spell_ids = filter_used_spells(state.all_spells, fights)
            return state
        })
    }, // extraReducers
}) // slice


export const {
    set_spells,
    set_spell_visible,
    update_used_spells,
    spell_selected,
} = SLICE.actions

export default SLICE.reducer


////////////////////////////////////////////////////////////////////////////////
// Extra Actions

export function load_spells(groups = []) {

    return async dispatch => {
        const spells = await API.load_spells(groups)
        dispatch(set_spells(spells))
    }
}
