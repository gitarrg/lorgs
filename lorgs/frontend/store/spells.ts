
import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import { createSelector } from 'reselect'
import Fight from '../types/fight'
import Spell from '../types/spell'

import { set_fights } from './fights'

const ICON_ROOT = "https://wow.zamimg.com/images/wow/icons/small"


interface SpellSliceState {
    /** all spells */
    all_spells: { [key: number] : Spell }

    /** id's of all spells that have been used */
    used_spell_ids: Number[]

    /** toggle for visible spells */
    spell_display: { [key: number] : boolean }

    /** all spells that are currently selected/focused */
    selected_spells: Number[]
}

// interface SpellMap { [key: number]: Spell }



////////////////////////////////////////////////////////////////////////////////
// Utils
//

/**
 * Group spells by spell_type
 */
export function group_spells_by_type(spells: { [key: number] : Spell } ) {

    const spells_by_type: { [key: string] : number[] } = {}

    Object.values(spells).forEach(spell => {
        const spell_type = spell.spell_type
        spells_by_type[spell_type] = spells_by_type[spell_type] || []
        spells_by_type[spell_type].push(spell.spell_id)
    })
    return spells_by_type
}


////////////////////////////////////////////////////////////////////////////////
// Actions
//

export function get_spell(state: any, spell_id: number) : Spell {
    return state.spells.all_spells[spell_id]
}


export function get_spells(state: any) : Spell[] {
    return state.spells.all_spells
}

/*
    Note: returns a new list each time. useMemo this one!
*/

export const get_spells_by_type = createSelector(
    get_spells,
    (spells) => {
        const v: { [key: string] : Spell[] } = {}
        Object.values(spells).forEach(spell => {
            v[spell.spell_type] = v[spell.spell_type] || []
            v[spell.spell_type].push(spell)

        })
        return v
    }
)


export function get_spell_visible(state: any, spell_id: number) : boolean {
    // undefined is considered true in this case
    return state.spells.spell_display[spell_id] !== false;
}

/* check if a given spell was ever used.
   Used to eg.: avoid creating spell buttons for ever possible trinket,
   even if nobody is using it.
*/
export function get_used_spells(state: any) : number[] {
    return state.spells.used_spell_ids
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
export function process_spells(spells?: { [key: number] : Spell } ) {
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

/**
 * Shared logic to append new spells to the slice
 */
function _add_spells_to_state(state: SpellSliceState , new_spells: { [key: number] : Spell } ) {

    new_spells = process_spells(new_spells)
    state.all_spells = {...state.all_spells, ...new_spells}

    Object.values(state.all_spells).forEach(spell => {
        state.spell_display[spell.spell_id] = spell.show;
    })
    return state

}


const INITIAL_STATE : SpellSliceState  = {
    all_spells: {},
    used_spell_ids: [],
    spell_display: {},
    selected_spells: [],
}


const SLICE = createSlice({
    name: "spells",

    initialState: INITIAL_STATE,

    reducers: {

        set_spells: (state, action) => {
            state = INITIAL_STATE
            return _add_spells_to_state(state, action.payload)
        },

        /**
         * Adds/Appends addition spells to the state
         *
         * @param {object} state current state
         * @param {object} action payload = spells to add
         * @returns new state
         */
        add_spells: (state, action) => {
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

        .addCase(set_fights, (state, action) => {
            const fights = action.payload

            state.used_spell_ids = filter_used_spells(fights)
            return state
        })

        /**
         * Add spells to slice when a spec was loaded
         */
        .addCase("specs/set_spec_spells", (state, action: any ) => {
            return _add_spells_to_state(state, action.payload.spells)
        })

        /**
         * Add spells to slice when a boss was loaded
         */
        .addCase("bosses/set_boss_spells", (state, action: any) => {
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
