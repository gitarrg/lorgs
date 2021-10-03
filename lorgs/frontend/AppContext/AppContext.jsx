

import React from 'react'

import create_skeleton_context from './skeleton_context.js'

// modes to switch some page related features
const MODES = {
    SPEC_RANKING: "spec_ranking",
    COMP_RANKING: "comp_ranking",
}


const DEFAULT_DATA  = {
    is_loading: true,

    mode: MODES.SPEC_RANKING,

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


    spells_list() {
        return Object.values(this.spells)
    },

    spells_by_type() {
        let types = {}
        this.spells_list().forEach(spell => {
            types[spell.spell_type] = (types[spell.spell_type] || {})
            types[spell.spell_type][spell.spell_id] = spell
        })
        return types
    },
}


// context to access the AppDataContext
const AppDataContext = React.createContext()


function getData() {
    return React.useContext(AppDataContext)
}


function AppContextProvider( {children }) {
    
    const [app_data, set_app_data] = React.useState(() => create_skeleton_context(DEFAULT_DATA))
    
    // attach function to update the state
    app_data.refresh = function() {
        set_app_data({...app_data})
    }

    // load global data
    React.useEffect(async () => {

        // console.time("request: specs")
        // app_data.SPECS = await api.load_specs()  // maybe for nav?
        // console.time("request: specs")
        // app_data.refresh()
    })

    return (
        <AppDataContext.Provider value={app_data}>
            {children}
        </AppDataContext.Provider>
    )
}


const AppContext = {
    AppContextProvider,
    getData,
    MODES,
}
export default AppContext

