

import React from "react"


export const DEFAULT_CONTEXT = {

    spells: {},
    fights: [],
    filters: {},

    show_casttime: true,
    show_duration: true,
    show_cooldown: true,

    get_fights_filtered: function() {
        console.log("Hey", this.fights)
        return this.fights.slice(0, 3)
    }
}

// export const DEFAULT_CONTEXT = AppContext
// DEFAULT_CONTEXT["spells"] = {}
// DEFAULT_CONTEXT["fights"] = []
// DEFAULT_CONTEXT["filters"] = {}







export const AppDataContext = React.createContext(DEFAULT_CONTEXT)
export default AppDataContext
