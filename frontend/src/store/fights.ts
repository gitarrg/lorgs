
import { createSlice } from '@reduxjs/toolkit'
import { createSelector } from 'reselect'
import { fetch_data } from '../api'
import type Actor from '../types/actor';
import type Fight from '../types/fight';
import type { AppDispatch, RootState } from './store'
import { MODES } from './ui'


////////////////////////////////////////////////////////////////////////////////
// Selectors
//

export function get_all_fights(state: RootState) : {[key: number]: Fight} {
    return state.fights.fights_by_id
}


export function get_fight_ids(state: RootState) {
    return state.fights.fight_ids
}


export function get_fight_is_loaded(state: RootState, fight_id: number) {
    return state.fights.fight_ids[fight_id] != undefined;
}


export const get_fights = createSelector<RootState, {[key: number]: Fight}, Fight[]>(
    get_all_fights,
    ( fights_by_id ) => {
        return Object.values(fights_by_id)
    }
)


/** Get all specs that occur in any of the fights */
export const get_occuring_specs = createSelector<RootState, Fight[], string[]>(
    get_fights,
    ( fights ) => {

        const specs_set = new Set<string>()

        fights.forEach(fight => {
            fight.players.forEach(player => {
                specs_set.add(player.spec)
            });
        })
        return Array.from(specs_set) // Set to Array
    }
)


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


function is_empty_fight(fight: Fight) {
    if (fight.players.some(player => player.casts.length > 0)) {
        return false;
    }
    // sorry bro
    return true
}


function _process_fight(fight: Fight) {
    if (fight.boss) {
        fight.boss = _process_actor(fight.boss)
        fight.boss.class = "boss"
    }
    fight.players = fight.players.map(actor => _process_actor(actor))
    return fight
}



function _process_fights(fights: Fight[]) {

    fights = fights.map(fight => _process_fight(fight))
    fights = fights.filter(fight => !is_empty_fight(fight))
    return fights
    // return fights.map(fight => _process_fight(fight))
}


const SLICE = createSlice({
    name: "fights",

    initialState: {
        fights: [] as Fight[],
        fights_by_id: {},
        fight_ids: [] as number[],
    },

    reducers: {
        set_fights: (state, action) => {

            const fights = _process_fights(action.payload ?? [])

            state.fights_by_id = {}
            state.fight_ids = []
            fights.forEach(fight => {
                state.fights_by_id[fight.fight_id] = fight
                state.fight_ids.push(fight.fight_id)
            })
            return state
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

    const url = `/api/spec_ranking/${spec_slug}/${boss_slug}?limit=100`;
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

    const url = `/api/comp_ranking/${boss_slug}${search}`;
    const fight_data = await fetch_data(url);
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


export function load_report_fights(report_id: string, search: string = "") {

    return async (dispatch: AppDispatch) => {
        dispatch({type: "ui/set_loading", payload: {key: "fights", value: true}})

        const url = `/api/user_reports/${report_id}/fights`;
        const report_data = await fetch_data(url, search)

        dispatch(set_fights(report_data.fights))
        dispatch({type: "ui/set_loading", payload: {key: "fights", value: false}})
    }
}
