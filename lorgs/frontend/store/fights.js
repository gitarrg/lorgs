
import { createSlice } from '@reduxjs/toolkit'

import API from '../api.js'
import { MODES, set_values } from './ui.js'


////////////////////////////////////////////////////////////////////////////////
// Actions
//

export function get_all_fights(state) {
    return state.fights
}

export const get_fights = get_all_fights;


////////////////////////////////////////////////////////////////////////////////
// Slice
//


const SLICE = createSlice({
    name: "fights",

    initialState: [],

    reducers: {
        set_fights: (state, action) => {


            // little hack to make sure the first fight always remains visible
            let fights = action.payload
            const [first_fight, ...others] = fights
            if (first_fight) {

                // extract the boss-fight
                let pinned_fight = {...first_fight}
                pinned_fight.pinned = true
                pinned_fight.players = []
                pinned_fight.boss.pinned = true

                // remove the boss from the original
                first_fight.boss = {}

                fights = [pinned_fight, first_fight, ...others]
            }


            return fights
        },
    }, // reducers

}) // slice


export const { set_fights } = SLICE.actions
export default SLICE.reducer


////////////////////////////////////////////////////////////////////////////////
// Extra Actions


export function load_fights(mode, {boss_slug, spec_slug, search}) {

    return async dispatch => {

        dispatch({type: "ui/set_loading", key: "fights", value: true})

        // load
        let fights = []
        switch (mode) {
            case MODES.SPEC_RANKING:
                fights = await API.load_spec_rankings(spec_slug, boss_slug)
                break;
            case MODES.COMP_RANKING:
                fights = await API.load_comp_rankings(boss_slug, search)
                break;
            default:
                break;
        } // switch

        // set
        dispatch(set_fights(fights))
        dispatch({type: "ui/set_loading", key: "fights", value: false})
    } // async dispatch
}
