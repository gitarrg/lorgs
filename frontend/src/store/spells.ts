import type Fight from '../types/fight'
import type { SpellDict } from '../types/spell'
import { RootState } from './store'
import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import { set_boss_spells } from './bosses'
import { set_fights } from './fights'
import { set_spec_spells } from './specs'


const ICON_ROOT = "https://wow.zamimg.com/images/wow/icons/medium"


export interface SpellSliceState {
    /** all spells */
    all_spells: SpellDict

    /** id's of all spells that have been used */
    used_spell_ids: number[]

    /** toggle for visible spells */
    spell_display: { [key: number] : boolean }

    /** all spells that are currently selected/focused */
    selected_spells: number[]

    spell_types: string[],
    spells_by_type: {[key: string]: number[]}
}


////////////////////////////////////////////////////////////////////////////////
// Actions
//

export function get_spell(state: RootState, spell_id: number) {
    return state.spells.all_spells[spell_id]
}


export function get_spells(state: RootState) {
    return state.spells.all_spells
}


export function get_spell_types(state: RootState) {
    return state.spells.spell_types
}


export function get_spells_for_type(state: RootState, spell_type: string) {
    return state.spells.spells_by_type[spell_type] || []
}


export function get_type_has_used_spells(state: RootState, spell_type: string) {

    const spell_ids = state.spells.spells_by_type[spell_type] || []
    const used_spells = state.spells.used_spell_ids
    return spell_ids.some(spell_id => used_spells.includes(spell_id))
}


export function get_spell_visible(state: RootState, spell_id: number) : boolean {
    // undefined is considered true in this case
    return state.spells.spell_display[spell_id] !== false;
}


/* check if a given spell was ever used.
   Used to eg.: avoid creating spell buttons for ever possible trinket,
   even if nobody is using it.
*/
export function get_used_spells(state: RootState) : number[] {
    return state.spells.used_spell_ids
}


export function get_spell_was_used(state: RootState, spell_id: number) {
    return state.spells.used_spell_ids.includes(spell_id)
}


export function filter_used_spells(fights: Fight[]) : number[] {

    if (!fights) { return [] }

    let used_spells = new Set<number>()
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
export function process_spells(spells?: SpellDict ) {
    if (!spells) { return {} }

    Object.values(spells).forEach(spell => {
        spell.specs = spell.specs || []
        spell.icon_path = spell.icon.startsWith("/") ? spell.icon : `${ICON_ROOT}/${spell.icon}`
    })
    return spells;
}


////////////////////////////////////////////////////////////////////////////////
// Slice
//

/* add a prefix to the input, to aid with sorting */
function _sort_spell_type_sort_key(spell_type: string) {

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
export function sort_spell_types(spell_types: string[]) {
    return spell_types.sort((a, b) => {
        const key_a = _sort_spell_type_sort_key(a)
        const key_b = _sort_spell_type_sort_key(b)
        return key_a > key_b ? 1 : -1
    })
}


/**
 * Shared logic to append new spells to the slice
 */
function _add_spells_to_state(state: SpellSliceState , new_spells: SpellDict ) {

    new_spells = process_spells(new_spells)
    state.all_spells = {...state.all_spells, ...new_spells}

    state.spells_by_type = {} // reset the list
    Object.values(state.all_spells).forEach(spell => {
        state.spells_by_type[spell.spell_type] = [...(state.spells_by_type[spell.spell_type] || []), spell.spell_id]

        const prev = state.spell_display[spell.spell_id]
        state.spell_display[spell.spell_id] = (prev === undefined) ? spell.show : prev // keep prev. value
    })

    state.spell_types = sort_spell_types(Object.keys(state.spells_by_type))

    return state
}


const INITIAL_STATE : SpellSliceState  = {
    all_spells: {},
    used_spell_ids: [],
    spell_display: {},
    selected_spells: [],

    spell_types: [],
    spells_by_type: {},

}


const SLICE = createSlice({
    name: "spells",

    initialState: INITIAL_STATE,

    reducers: {

        set_spells: (state, action: PayloadAction<SpellDict>) => {
            const new_state = {...INITIAL_STATE}
            return _add_spells_to_state(new_state, action.payload)
        },

        /**
         * Adds/Appends addition spells to the state
         *
         * @param {object} state current state
         * @param {object} action payload = spells to add
         * @returns new state
         */
        add_spells: (state, action: PayloadAction<SpellDict>) => {
            return _add_spells_to_state(state, action.payload)
        },

        update_used_spells: (state, action: PayloadAction<{fights: Fight[] }>) => {
            const {fights} = action.payload
            state.used_spell_ids = filter_used_spells(fights)
            return state
        },

        set_spell_visible: (state, action: PayloadAction<{spell_id: number, visible: boolean}> ) => {
            const { spell_id, visible } = action.payload
            state.spell_display[spell_id] = visible
            return state;
        },

        spell_selected: (state, action: PayloadAction<{spell_id: number, selected: boolean, deselect_others?: boolean }>) => {
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

        .addCase(set_fights, (state, action: PayloadAction<Fight[]> ) => {
            const fights = action.payload
            state.used_spell_ids = filter_used_spells(fights)
            return state
        })

        /**
         * Add spells to slice when a spec was loaded
         */
        .addCase(set_spec_spells, (state, action: PayloadAction<{spells: SpellDict}> ) => {
            return _add_spells_to_state(state, action.payload.spells)
        })

        /**
         * Add spells to slice when a boss was loaded
         */
        .addCase(set_boss_spells, (state, action: PayloadAction<{spells: SpellDict}>) => {
            return _add_spells_to_state(state, action.payload.spells)
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
