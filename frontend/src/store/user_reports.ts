import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import { createSelector } from 'reselect'

import { fetch_data } from '../api'
import { AppDispatch, RootState } from './store'
import type Actor from '../types/actor'
import type Fight from '../types/fight'


export interface UserReportData {
    is_loading: boolean
    title: string
    report_id: string
    fights: Fight[]
    players: Actor[]

    /**id of the task when loading the data */
    task_id?: string
}


////////////////////////////////////////////////////////////////////////////////
// Utils
//
export interface UserReportSearchParams {
    player_ids: number[]
    fight_ids: number[]
}


export function build_url_search_string(params: UserReportSearchParams) {

    let search = new URLSearchParams({})
    params.fight_ids.forEach(fight_id => { search.append("fight", fight_id.toString()) })
    params.player_ids.forEach(player_id => { search.append("player", player_id.toString()) })
    return search.toString()
}


////////////////////////////////////////////////////////////////////////////////
// Selectors
//

/** Gets the entire user report data.
 * Not intended to be used directly. Just a starting point for all other selectors.
 */
export function get_user_report(state: RootState) {
    return state.user_report
}


export function get_report_id(state: RootState) {
    return state.user_report.report_id
}


export function get_is_loading(state: RootState) {
    return state.user_report.is_loading
}


export const get_user_report_fights = createSelector<RootState, UserReportData, Fight[]>(
    get_user_report,
    (user_report) => {
        return user_report.fights
    }
)


export const get_user_report_players = createSelector<RootState, UserReportData, Actor[]>(
    get_user_report,
    (user_report) => {
        return user_report.players
    }
)


////////////////////////////////////////////////////////////////////////////////
// Slice
//

const INITIAL_STATE: UserReportData = {
    title: "",
    report_id: "",
    fights: [],
    players: [],
    task_id: "",
    is_loading: false,
}


const SLICE = createSlice({
    name: "user_report",

    initialState: INITIAL_STATE,

    reducers: {

        set_report_id: (state, action: PayloadAction<string>) => {

            state.report_id = action.payload
            return state;
        },

        report_overview_loading_started: (state, action: PayloadAction<boolean>) => {
            state.is_loading = action.payload
            return state
        },

        report_overview_loaded: (state, action: PayloadAction<UserReportData>) => {
            console.log("report_loaded", action)
            return {
                ...state,
                ...action.payload,
                is_loading: false,
            }
        }, // fights_loaded
    },
})

export default SLICE.reducer

export const {
    set_report_id,
    report_overview_loading_started,
} = SLICE.actions


////////////////////////////////////////////////////////////////////////////////
// Extra Actions

/** Load a given user report */
export function load_report_overview(report_id: string) {

    return async (dispatch: AppDispatch) => {

        // update loading state
        dispatch(SLICE.actions.report_overview_loading_started(true))

        // Try to get existing one
        const url = `/api/user_reports/${report_id}/load_overview`;
        const report_data = await fetch_data(url);

        // store result
        dispatch(SLICE.actions.report_overview_loaded(report_data))
    }
}


export function load_report(report_id: string, fight_ids: number[], player_ids: number[]) {


    return async (dispatch: AppDispatch) => {

        const search_string = build_url_search_string({report_id, fight_ids, player_ids})
        const url = `/api/user_reports/${report_id}/load?${search_string}`;
        let response = await fetch_data(url);
        return response
    }
}

