import type { RootState } from './store'
import { createSelector } from 'reselect'
import { createSlice, PayloadAction } from '@reduxjs/toolkit'


// modes to switch some page related features
export const MODES = {
    NONE: "none",
    SPEC_RANKING: "spec_ranking",
    COMP_RANKING: "comp_ranking",
    USER_REPORT: "user_report",
}

export type Mode = "none" | "spec_ranking" | "comp_ranking"


// TODO: ModeSettings should be in some "constants"-file

interface ModeSetting {
    /** space in pixels between each fight row */
    fight_space: number
}

const MODE_SETTINGS: {[key: string]: ModeSetting } = {}


const default_setting: ModeSetting = {
    fight_space: 10,
}

MODE_SETTINGS[MODES.NONE] = default_setting

MODE_SETTINGS[MODES.SPEC_RANKING] = {
    ...default_setting,
    fight_space: 0,
}

MODE_SETTINGS[MODES.COMP_RANKING] = default_setting
MODE_SETTINGS[MODES.USER_REPORT] = default_setting



////////////////////////////////////////////////////////////////////////////////
// Actions
//
export function get_mode(state: RootState) {
    return state.ui.mode
}

export function get_mode_setting(state: RootState) {
    return MODE_SETTINGS[state.ui.mode] || default_setting
}


export function get_difficulty(state: RootState) {
    return state.ui.difficulty
}


export function get_filters(state: RootState) {
    return state.ui.filters
}


export const get_is_loading = createSelector(
    (state: RootState) => state.ui._loading, // dependency
    (loading_state) => {
        return Object.values(loading_state).some(v => v == true)
    }
)


export function get_tooltip(state: RootState) {
    return state.ui.tooltip
}


////////////////////////////////////////////////////////////////////////////////
// Slice
//
type FilterGroup =
    | "role"
    |  "spec"
    | "class"
    | "covenant"


export interface FilterValues {

    killtime: {min: number | null, max: number | null}

    /** Filter Groups like:
     * role: { tank: false, heal: true}
     * spec: { holy-paladin: true}
     */
    role: {[key: string]: boolean}
    spec: {[key: string]: boolean}
    class: {[key: string]: boolean}
    covenant: {[key: string]: boolean}
}


export interface UiSliceState {

    mode: "none" | "spec_ranking" | "comp_ranking"

    /** elements that are loading */
    _loading: { [key: string]: boolean }

    /** currently selected spec */
    spec_slug: string

    /** currently selected boss */
    boss_slug: string

    /** selected difficulty */
    difficulty: string

    // Timeline Options
    settings: { [key: string]: boolean}

    // fight/player filter settings
    filters: FilterValues // { [key: string]: { [key: string]: boolean | null } }

    tooltip: {
        content: string
        position: {x: number, y: number}
    }
}


const INITIAL_STATE: UiSliceState = {

    mode: "none",

    _loading: {}, // elements that are loading

    spec_slug: "", // currently selected spec
    boss_slug: "", // currently selected boss
    difficulty: "mythic", // currently selected difficulty

    // Timeline Options
    settings: {
        show_casticon: true,
        show_casttime: true,
        show_duration: true,
        show_cooldown: true,
    },

    // fight/player filter settings
    filters: {

        // player filters
        role: {},
        class: {},
        spec: {},
        covenant: {},

        // fight filters
        killtime: {min: null, max: null},
    },

    tooltip: {
        content: "",
        position: {x: 0, y: 0}
    }
}


const SLICE = createSlice({
    name: "ui",

    initialState: INITIAL_STATE,

    reducers: {

        set_boss_slug: (state, action: PayloadAction<string>) => {
            state.boss_slug = action.payload
            return state
        },

        set_spec_slug: (state, action: PayloadAction<string>) => {
            state.spec_slug = action.payload
            return state
        },

        set_difficulty: (state, action: PayloadAction<string>) => {
            state.difficulty = action.payload
            return state
        },

        update_settings: (state, action) => {
            state.settings = {...state.settings, ...action.payload}
            return state
        },

        // Filters
        set_filter: (state, action: PayloadAction<{group: FilterGroup, name: string, value: boolean}>) => {
            const { group, name, value } = action.payload
            state.filters[group] = state.filters[group] || {}
            state.filters[group][name] = value
            return state
        },

        set_filters: (state, action) => {
            state.filters = {...state.filters, ...action.payload}
            return state
        },

        // loading
        set_loading: (state, action: PayloadAction<{key: string, value: boolean}>) => {
            state._loading[action.payload.key] = action.payload.value
            return state
        },

        set_mode: (state, action) => {
            state.mode = action.payload
            return state
        },

        set_tooltip: (state, action) => {
            const {content, position } = action.payload
            state.tooltip.content = content
            state.tooltip.position = position
            return state
        }
    }, // reducers
}) // slice


export const {
    set_boss_slug,
    set_difficulty,
    set_filter,
    set_filters,
    set_mode,
    set_spec_slug,
    set_tooltip,
    update_settings,
} = SLICE.actions


export default SLICE.reducer
