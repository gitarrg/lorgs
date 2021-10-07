/*
Redux Data Store
*/

import { createStore } from 'redux'
import API from './api'
import { apply_filters } from './AppContext/filter_logic'


// modes to switch some page related features
export const MODES = {
    NONE: "none",
    SPEC_RANKING: "spec_ranking",
    COMP_RANKING: "comp_ranking",
}


const DEFAULT_STATE  = {

    is_loading: true,

    mode: MODES.NONE,

    boss: { spells: [] },
    spec: {},

    bosses: [],
    roles: [],

    // specs currently loaded
    specs: [],

    spells: {},
    fights: [],

    // all (display)-filters
    filters: {
        role: {}, // filters based on roles
        spec: {}, // based on spec
    },

    show_casttime: true,
    show_duration: true,
    show_cooldown: true,
}


////////////////////////////////////////////////////////////////////////////////
// REDCUER
//

function set_object_attribute(state, attr, value) {
    // set a given attribute inside the state
    let new_state = {...state}
    new_state[attr] = value
    return new_state
}


function set_filter_attribute(state, attr, value) {
    // updates a value inside the filters subobject
    let new_filters = set_object_attribute(state.filters, attr, value)
    return set_object_attribute(state, "filters", new_filters)
}


function filters_apply(state) {
    let new_state = {...state}
    apply_filters(new_state, new_state.fights, new_state.filters)
    return new_state

}


function reducer(state = DEFAULT_STATE, action) {
    
    // console.log("reducer", action, action.value)
    // console.log("reducer|STATE", state)

    switch (action.type) {

        // generic update value
        case "update_value":
            return set_object_attribute(state, action.field, action.value)
            
        case "update_filter":
            const new_state = set_filter_attribute(state, action.field, action.value)
            return filters_apply(new_state)
            // state.filters[action.field] = action.value
            // state.filters = {...state.filters}
            // state = {...state}
            // break;
        case "filters/apply":
            return filters_apply({...state})

        case "process_fetched_data":
            return API.process_fetched_data({...state})
    
        default:
            console.log("unsupported action type:", action.type)
            return state
    } // switch
}

const data_store = createStore(
    reducer,
    window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__()
)
export default data_store

