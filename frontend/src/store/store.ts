/*
Redux Data Store
*/

import { configureStore } from '@reduxjs/toolkit'

import bosses_reducer from "./bosses"
import classes_reducer from "./classes"
import fights_reducer from "./fights"
import roles_reducer from "./roles"
import specs_reducer from "./specs"
import spells_reducer from "./spells"
import status_reducer from "./status"
import ui_reducer from "./ui"
import user_reducer from "./user"
import user_report_reducer from "./user_reports"


////////////////////////////////////////////////////////////////////////////////
// REDCUER
//
const LORRGS_DEBUG = "LORRGS_DEBUG" in window


const store = configureStore({

    // preloadedState: DEFAULT_STATE,
    reducer: {
        classes: classes_reducer,
        fights: fights_reducer,
        raid_zone: bosses_reducer,
        roles: roles_reducer,
        specs: specs_reducer,
        spells: spells_reducer,
        status: status_reducer,
        ui: ui_reducer,
        user: user_reducer,
        user_report: user_report_reducer,
    },
    devTools: LORRGS_DEBUG,
})

export default store


// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>
// Inferred type: {posts: PostsState, comments: CommentsState, users: UsersState}
export type AppDispatch = typeof store.dispatch
