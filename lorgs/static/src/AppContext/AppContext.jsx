

import React from 'react'

import create_skeleton_context from './skeleton_context.js'


const DEFAULT_DATA  = {
    is_loading: true,
    
    spells: {},
    fights: [],
    filters: {},
    
    show_casttime: true,
    show_duration: true,
    show_cooldown: true,
}


// context to access the AppDataContext
const AppDataContext = React.createContext()


function getData() {
    return React.useContext(AppDataContext)
}


function AppContextProvider( {children }) {
    
    const [stateData, setStateData] = React.useState(() => create_skeleton_context(DEFAULT_DATA))
    
    // attach function to update the state
    stateData.refresh = function() {
        setStateData({...stateData})
    }

    return (
        <AppDataContext.Provider value={stateData}>
            {children}
        </AppDataContext.Provider>
    )
}


const AppContext = {
    AppContextProvider,
    getData,
}
export default AppContext

