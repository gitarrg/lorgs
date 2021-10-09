
import { createSlice } from '@reduxjs/toolkit'
import API from '../api.js'


const EMPTY_BOSS = {
    spells: [],
    class: {},
}


////////////////////////////////////////////////////////////////////////////////
// Selectors
//

export function get_bosses(state) {
    return state.bosses
}


export function get_boss(state, boss_slug) {
    boss_slug = boss_slug || state.ui.boss_slug
    return state.bosses[boss_slug] || EMPTY_BOSS
}


////////////////////////////////////////////////////////////////////////////////
// Slice
//

function _post_process_boss(boss) {

    boss.spells = boss.spells || []
    boss.spells_by_type = { boss: boss.spells}
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
    },
})

export const { set_bosses, set_boss } = SLICE.actions
export default SLICE.reducer


////////////////////////////////////////////////////////////////////////////////
// Extra Actions

/* load all bosses */
export function load_bosses() {

    return async dispatch => {
        const bosses = await API.load_bosses()
        dispatch(set_bosses(bosses))
    }
}
