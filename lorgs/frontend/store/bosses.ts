
import { createSlice } from '@reduxjs/toolkit'
import { group_spells_by_type } from './spells'
import { fetch_data } from '../api'

import Boss from "../types/boss"


interface BossesSliceState {
    [key: string]: Boss
}


////////////////////////////////////////////////////////////////////////////////
// Selectors
//

export function get_bosses(state) : BossesSliceState {
    return state.bosses
}


export function get_boss(state, boss_slug: string) : Boss {
    boss_slug = boss_slug || state.ui.boss_slug
    return state.bosses[boss_slug] || null
}


////////////////////////////////////////////////////////////////////////////////
// Slice
//

function _post_process_boss(boss: Boss) {
    boss.loaded = false
    boss.icon_path = `/static/images/bosses/sanctum-of-domination/${boss.full_name_slug}.jpg`
    return boss
}


const SLICE = createSlice({
    name: "bosses",

    initialState: {} as BossesSliceState,

    reducers: {

        set_bosses: (state, action) => {

            // array to object (by full_name_slug)
            action.payload.forEach(boss => {
                state[boss.full_name_slug] = _post_process_boss(boss)

            });
            return state
        },

        set_boss: (state, action) => {
            const boss = _post_process_boss(action.payload)
            state[boss.full_name_slug] = boss
            return state
        },

        set_boss_spells: (state, action) => {
            const {boss_slug, spells} = action.payload
            const boss = state[boss_slug]
            if (!boss) { return }

            boss.spells_by_type =  group_spells_by_type(spells)
            boss.loaded = true
            return state
        }
    },
})

export default SLICE.reducer


////////////////////////////////////////////////////////////////////////////////
// Extra Actions

/* load all bosses */
export function load_bosses() {

    return async dispatch => {

        dispatch({type: "ui/set_loading", key: "bosses", value: true})

        // Request
        const zone_info = await fetch_data(`/api/bosses`);
        const bosses = zone_info.bosses || []

        dispatch(SLICE.actions.set_bosses(bosses))
        dispatch({type: "ui/set_loading", key: "bosses", value: false})
    }
}


/**
 * Load Spells for a given boss
 * @param {string} boss_slug name of the boss whom's spells to load
 */
export function load_boss_spells(boss_slug: string) {

    return async dispatch => {

        dispatch({type: "ui/set_loading", key: "boss_spells", value: true})

        // Request
        const spells = await fetch_data(`/api/boss/${boss_slug}/spells`);

        dispatch(SLICE.actions.set_boss_spells({boss_slug, spells}))
        dispatch({type: "ui/set_loading", key: "boss_spells", value: false})
    }
}
