
import { createSlice } from '@reduxjs/toolkit'

import { fetch_data } from '../api'
import type Actor from '../types/actor';
import type Fight from '../types/fight';
import type { AppDispatch, RootState } from './store'
import { MODES } from './ui'


////////////////////////////////////////////////////////////////////////////////
// Actions
//

export function get_all_fights(state: RootState) : Fight[] {
    return state.fights
}

export const get_fights = get_all_fights;


////////////////////////////////////////////////////////////////////////////////
// Slice
//
function _process_actor(actor: Actor) {

    const spell_counter: {[key: number]: number} = {}
    actor.casts = actor.casts || []
    actor.casts.forEach(cast => {
        cast.counter = spell_counter[cast.id] = (spell_counter[cast.id] || 0) + 1
    })
    return actor
}


function _process_fight(fight: Fight) {
    fight.boss = fight.boss && _process_actor(fight.boss)
    fight.players = fight.players.map(actor => _process_actor(actor))
    return fight
}

function _process_fights(fights: Fight[]) {
    return fights.map(fight => _process_fight(fight))
}


const SLICE = createSlice({
    name: "fights",

    initialState: [] as Fight[],

    reducers: {
        set_fights: (_, action) => {
            return _process_fights(action.payload)
        },
    }, // reducers

}) // slice


export const { set_fights } = SLICE.actions
export default SLICE.reducer


////////////////////////////////////////////////////////////////////////////////
// Extra Actions

function _pin_first_fight(fights: Fight[]) {
    // little hack to make sure the first fight always remains visible
    if (fights.length == 0) { return fights }

    const [first_fight, ...others] = fights
    // extract the boss-fight
    let pinned_fight = {...first_fight}
    pinned_fight.pinned = true
    pinned_fight.players = []
    if (pinned_fight.boss) {
        pinned_fight.boss.pinned = true
    }

    // remove the boss from the original
    first_fight.boss = undefined
    return [pinned_fight, first_fight, ...others]
}


async function _load_spec_rankings(spec_slug : string, boss_slug: string) {

    let url = `/api/spec_ranking/${spec_slug}/${boss_slug}?limit=100`;
    const fight_data: {fights: Fight[]} = await fetch_data(url);

    // post process
    return fight_data.fights.map((fight, i) => {
        fight.players.forEach(player => {
            player.rank = i+1  // insert ranking data
        })
        return fight
    })
}


async function _load_comp_rankings(boss_slug : string, search="") {

    let url = `/api/comp_ranking/${boss_slug}${search}`;
    let response = await fetch(url);
    if (response.status != 200) {
        return [];
    }
    const fight_data = await response.json();
    return fight_data.fights || []
}


export function load_fights(mode: string, {boss_slug, spec_slug="", search=""} : {boss_slug: string, spec_slug?: string, search?: string} ) {

    return async (dispatch: AppDispatch) => {

        dispatch({type: "ui/set_loading", payload: {key: "fights", value: true}})

        // load
        let fights = []
        switch (mode) {
            case MODES.SPEC_RANKING:
                fights = await _load_spec_rankings(spec_slug, boss_slug)
                fights = _pin_first_fight(fights)
                break;
                case MODES.COMP_RANKING:
                fights = await _load_comp_rankings(boss_slug, search)
                break;
            default:
                break;
        } // switch

        // set
        dispatch(set_fights(fights))
        dispatch({type: "ui/set_loading", payload: {key: "fights", value: false}})
    } // async dispatch
}
