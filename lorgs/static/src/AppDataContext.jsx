

import React, { useState, useContext } from "react"



export const DEFAULT_CONTEXT = {}
DEFAULT_CONTEXT["spells"] = {}
DEFAULT_CONTEXT["fights"] = {}


export const AppDataContext = React.createContext(DEFAULT_CONTEXT)
export default AppDataContext


export function AppDataContextProvider({children}) {

    // const [data, setData] = useState({"x": 3})


    return (
        <AppDataContext.Provider value={{ data, setData }}>
            {children}
        </AppDataContext.Provider>
    )
  


}

// {
//     spells: ["default"] // list of all spell-data dicts
// });


// export const AppDataProvider = AppDataContext.Provider
//  AppDataContext

