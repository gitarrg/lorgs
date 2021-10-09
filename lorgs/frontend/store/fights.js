
import { createSlice } from '@reduxjs/toolkit'
import API from '../api.js'
import { MODES, set_values } from './ui.js'


////////////////////////////////////////////////////////////////////////////////
// Actions
//

export function get_fights(state) {
    return state.fights
}


////////////////////////////////////////////////////////////////////////////////
// Slice
//


const SLICE = createSlice({
    name: "fights",

    initialState: [],

    reducers: {
        set_fights: (state, action) => {
            return action.payload
        },
    },
})


export const { set_fights } = SLICE.actions
export default SLICE.reducer


////////////////////////////////////////////////////////////////////////////////
// Extra Actions


export function load_fights(mode, {boss_slug, spec_slug}) {
    return async dispatch => {
        // load
        let fights = []
        switch (mode) {
            case MODES.SPEC_RANKING:
                fights = await API.load_spec_rankings(spec_slug, boss_slug)

            default:
                break;
            }

        // set
        dispatch(set_fights(fights))
        dispatch(set_values({is_loading: false}))

    }
}
