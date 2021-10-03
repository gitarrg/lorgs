/*
Redux Data Store
*/

import { createStore } from 'redux'

const DEFAULT_STATE  = {
    is_loading: true,

    // mode: MODES.SPEC_RANKING,

    boss: {
        spells: [],
    },

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


/*     spells_list() {
        return Object.values(this.spells)
    },

    spells_by_type() {
        let types = {}
        this.spells_list().forEach(spell => {
            types[spell.spell_type] = (types[spell.spell_type] || {})
            types[spell.spell_type][spell.spell_id] = spell
        })
        return types
    }, */
}


function reducer(state = DEFAULT_STATE, action) {
    console.log("reducer", action, action.value)
    console.log("reducer|STATE", state)
    
    switch (action.type) {

        case "update_value":
            state[action.field] = action.value
            state = {...state}
            break;
            
        case "update_filter":
            state.filters[action.field] = action.value
            console.log("new value", state.filters)
            state.filters = {...state.filters}
            state = {...state}
            break;
    
        default:
            console.log("unsupported action type:", action.type)
            break;
    } // switch

    return state

}

const data_store = createStore(reducer)
export default data_store

