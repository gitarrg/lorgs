
import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import type Boss from "../types/boss"
import type { AppDispatch, RootState } from './store'
import { fetch_data } from '../api'
import { group_spells_by_type } from './store_utils'
import { ZONE_ID } from '../constants'
import type RaidZone from '../types/raid_zone'


////////////////////////////////////////////////////////////////////////////////
// Selectors
//

/** all bosses in the zone, keyed by their full_name_slug */
export function get_bosses(state: RootState) {
    return state.raid_zone.bosses
}

/** a single boss from the zone (defaults to the currently selected boss) */
export function get_boss(state: RootState, boss_slug?: string) {
    boss_slug = boss_slug ?? state.ui.boss_slug
    return state.raid_zone.bosses[boss_slug] || null
}


////////////////////////////////////////////////////////////////////////////////
// Slice
//

function _post_process_boss(zone: RaidZone, boss: Boss) {
    boss.loaded = false
    boss.icon_path = `/static/img/bosses/${zone.name_slug}/${boss.full_name_slug}.jpg`

    // insert some static data
    boss.role = "boss"
    boss.class = { name: "boss", name_slug: "boss"}
}


const INITIAL_STATE: RaidZone = {
    id: -1,
    name: "",
    name_slug: "",
    bosses: {},
}


interface RaidZoneAPIResponse {
    id: -1,
    name: "",
    name_slug: "",
    bosses: Boss[],
}


const SLICE = createSlice({
    name: "raid_zone",

    initialState: INITIAL_STATE,

    reducers: {

        set_zone: (state, action: PayloadAction<RaidZoneAPIResponse> ) => {

            state.id        = action.payload.id
            state.name      = action.payload.name
            state.name_slug = action.payload.name_slug

            // array to object (by full_name_slug)
            action.payload.bosses.forEach(boss => {
                _post_process_boss(state, boss)
                state.bosses[boss.full_name_slug] = boss
            });
            return state
        },

        set_boss_spells: (state, action) => {
            const {boss_slug, spells} = action.payload
            const boss = state.bosses[boss_slug]
            if (!boss) { return }

            boss.spells_by_type =  group_spells_by_type(spells, boss)
            boss.loaded = true
            return state
        }
    },
})

export const {
    set_boss_spells
} = SLICE.actions

export default SLICE.reducer


////////////////////////////////////////////////////////////////////////////////
// Extra Actions

/* load all bosses */
export function load_bosses() {

    return async (dispatch: AppDispatch) => {

        dispatch({type: "ui/set_loading", payload: {key: "zone", value: true}})

        // Request
        const zone_info = await fetch_data(`/api/zones/${ZONE_ID}`);

        dispatch(SLICE.actions.set_zone(zone_info))
        dispatch({type: "ui/set_loading", payload: {key: "zone", value: false}})
    }
}


/**
 * Load Spells for a given boss
 * @param {string} boss_slug name of the boss whom's spells to load
 */
export function load_boss_spells(boss_slug: string) {

    return async (dispatch: AppDispatch) => {

        const load_key = `boss/${boss_slug}`
        dispatch({type: "ui/set_loading", payload: {key: load_key, value: true}})

        // Request
        const spells: RaidZoneAPIResponse = await fetch_data(`/api/bosses/${boss_slug}/spells`);

        dispatch(SLICE.actions.set_boss_spells({boss_slug, spells}))
        dispatch({type: "ui/set_loading", payload: {key: load_key, value: false}})
    }
}
