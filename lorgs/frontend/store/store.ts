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

export default configureStore({

    // preloadedState: DEFAULT_STATE,
    reducer: {
        bosses: bosses_reducer,
        fights: fights_reducer,
        roles: roles_reducer,
        specs: specs_reducer,
        spells: spells_reducer,
        ui: ui_reducer,
    },
    devTools: LORRGS_DEBUG,
})
