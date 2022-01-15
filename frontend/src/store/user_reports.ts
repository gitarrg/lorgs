import type Actor from '../types/actor'
import type Fight from '../types/fight'
import { AppDispatch, RootState } from './store'
import { createSelector } from 'reselect'
import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import { fetch_data } from '../api'


export interface UserReportData {
    is_loading: boolean

    /** optional error message */
    error?: string,

    title: string
    report_id: string

    fights: {[key: string]: Fight}
    players: {[key: string]: Actor}

    /**id of the task when loading the data */
    task_id?: string

    /**unix timestamp, when the report was created */
    date: number

    /** name of the guild this report belongs to */
    guild?: string

    /** user who logged this report */
    owner: string
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
    search.append("fight", params.fight_ids.join("."))
    search.append("player", params.player_ids.join("."))
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
        return Object.values(user_report.fights)
    }
)


export const get_user_report_players = createSelector<RootState, UserReportData, Actor[]>(
    get_user_report,
    (user_report) => {
        return Object.values(user_report.players)
    }
)

////////////////////////////////////////////////////////////////////////////////
// Slice
//

const INITIAL_STATE: UserReportData = {
    title: "",
    report_id: "",
    fights: {},
    players: {},
    task_id: "",
    owner: "",
    is_loading: false,
    date: 0,

    error: "",
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
            // using initial state, to clear out previously loaded values
            return {
                ...INITIAL_STATE,
                ...action.payload,
                is_loading: false,
            }
        }, // report_overview_loaded
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
export function load_report_overview(report_id: string, refresh?: boolean) {

    return async (dispatch: AppDispatch) => {

        // update loading state
        dispatch(SLICE.actions.report_overview_loading_started(true))

        // Try to get existing one
        const url = `/api/user_reports/${report_id}/load_overview`;

        const report_data = await fetch_data(url, {refresh: refresh || false});

        // store result
        dispatch(SLICE.actions.report_overview_loaded(report_data))
    }
}


export function load_report(report_id: string, fight_ids: number[], player_ids: number[], user_id?: string) {

    return async (dispatch: AppDispatch) => {

        const search_string = build_url_search_string({fight_ids, player_ids})
        let url = `/api/user_reports/${report_id}/load?${search_string}`;
        if (user_id) {
            url = `${url}&user_id=${user_id}`
        }
        let response = await fetch_data(url);
        return response
    }
}

