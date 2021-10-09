
import { createSlice, createSelector } from '@reduxjs/toolkit'
// import { createSelector } from 'reselect'

import API from '../api.js'
import { get_filters, MODES, set_values } from './ui.js'


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
            return action.payload
        },
    }, // reducers

}) // slice


export const { set_fights } = SLICE.actions
export default SLICE.reducer


////////////////////////////////////////////////////////////////////////////////
// Extra Actions


export function load_fights(mode, {boss_slug, spec_slug, search}) {

    return async dispatch => {
        // load
        let fights = []
        switch (mode) {
            case MODES.SPEC_RANKING:
                fights = await API.load_spec_rankings(spec_slug, boss_slug)
            case MODES.COMP_RANKING:
                fights = await API.load_comp_rankings(boss_slug, search)
            default:
                break;
        } // switch

        // set
        dispatch(set_fights(fights))
        dispatch(set_values({is_loading: false}))
    } // async dispatch
}
