/*
Redux Data Store
*/

import { configureStore } from '@reduxjs/toolkit'

import bosses_reducer from "./bosses"
import fights_reducer from "./fights"
import roles_reducer from "./roles"
import specs_reducer from "./specs"
import spells_reducer from "./spells"
import ui_reducer from "./ui"


////////////////////////////////////////////////////////////////////////////////
// REDCUER
//
const LORRGS_DEBUG = "LORRGS_DEBUG" in window


const store = configureStore({

    // preloadedState: DEFAULT_STATE,
    reducer: {
        raid_zone: bosses_reducer,
        fights: fights_reducer,
        roles: roles_reducer,
        specs: specs_reducer,
        spells: spells_reducer,
        ui: ui_reducer,
    },
    devTools: LORRGS_DEBUG,
})

export default store


// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>
// Inferred type: {posts: PostsState, comments: CommentsState, users: UsersState}
export type AppDispatch = typeof store.dispatch
