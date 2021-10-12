
import { createSlice } from '@reduxjs/toolkit'
import API from '../api.js'
import { group_spells_by_type } from './spells.js'


////////////////////////////////////////////////////////////////////////////////
// Selectors
//

export function get_bosses(state) {
    return state.bosses
}


export function get_boss(state, boss_slug) {
    boss_slug = boss_slug || state.ui.boss_slug
    return state.bosses[boss_slug] || null
}


////////////////////////////////////////////////////////////////////////////////
// Slice
//

function _post_process_boss(boss) {
    boss.loaded = false
    boss.icon_path = `/static/images/bosses/sanctum-of-domination/${boss.full_name_slug}.jpg`
    return boss
}


const SLICE = createSlice({
    name: "bosses",

    initialState: {},

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

        const bosses = await API.load_bosses()
        dispatch(SLICE.actions.set_bosses(bosses))
        dispatch({type: "ui/set_loading", key: "bosses", value: false})
    }
}


/**
 * Load Spells for a given boss
 * @param {string} boss_slug name of the boss whom's spells to load
 */
export function load_boss_spells(boss_slug) {

    return async dispatch => {

        dispatch({type: "ui/set_loading", key: "boss_spells", value: true})
        const spells = await API.load_boss_spells(boss_slug)
        dispatch(SLICE.actions.set_boss_spells({boss_slug, spells}))
        dispatch({type: "ui/set_loading", key: "boss_spells", value: false})
    }
}
