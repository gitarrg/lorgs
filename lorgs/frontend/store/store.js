/*
Redux Data Store
*/

import { configureStore } from '@reduxjs/toolkit'

import bosses_reducer from "./bosses.js"
import fights_reducer from "./fights.js"
import roles_reducer from "./roles.js"
import specs_reducer from "./specs.js"
import spells_reducer from "./spells.js"
import ui_reducer from "./ui.js"



////////////////////////////////////////////////////////////////////////////////
// REDCUER
//

export default configureStore({

    // preloadedState: DEFAULT_STATE,
    reducer: {
        ui: ui_reducer,
        bosses: bosses_reducer,
        fights: fights_reducer,
        roles: roles_reducer,
        specs: specs_reducer,
        spells: spells_reducer,
    },
    devTools: LORRGS_DEBUG,
})
