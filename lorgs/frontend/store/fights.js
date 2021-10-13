
import { createSlice } from '@reduxjs/toolkit'

import API from '../api.js'
import { MODES } from './ui.js'


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
function _process_actor(actor) {

    const spell_counter = {}
    actor.casts = actor.casts || []
    actor.casts.forEach(cast => {
        cast.counter = spell_counter[cast.id] = (spell_counter[cast.id] || 0) + 1
    })
    return actor
}


function _process_fight(fight) {
    fight.boss = _process_actor(fight.boss)
    fight.players = fight.players.map(actor => _process_actor(actor))
    return fight
}

function _process_fights(fights) {
    return fights.map(fight => _process_fight(fight))
}


const SLICE = createSlice({
    name: "fights",

    initialState: [],

    reducers: {
        set_fights: (state, action) => {
            return _process_fights(action.payload)
        },
    }, // reducers

}) // slice


export const { set_fights } = SLICE.actions
export default SLICE.reducer


////////////////////////////////////////////////////////////////////////////////
// Extra Actions

function _pin_first_fight(fights) {
    // little hack to make sure the first fight always remains visible
    if (fights.length == 0) { return fights }

    const [first_fight, ...others] = fights
    // extract the boss-fight
    let pinned_fight = {...first_fight}
    pinned_fight.pinned = true
    pinned_fight.players = []
    pinned_fight.boss.pinned = true

    // remove the boss from the original
    first_fight.boss = {}
    return [pinned_fight, first_fight, ...others]
}


export function load_fights(mode, {boss_slug, spec_slug, search}) {

    return async dispatch => {

        dispatch({type: "ui/set_loading", key: "fights", value: true})

        // load
        let fights = []
        switch (mode) {
            case MODES.SPEC_RANKING:
                fights = await API.load_spec_rankings(spec_slug, boss_slug)
                fights = _pin_first_fight(fights)
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
