

import React from 'react'


export const ButtonGroupContext = React.createContext()


export default function ButtonGroup({name, extra_class, className, side="left", children}) {

    ///////////////////////
    // Hooks

    // The Groups Active state:
    // in addition to the "group_active"-value, we pass a "group_source",
    // which can be used to determine who changed the groups state.
    const [{group_active, group_source}, setActive] = React.useState({group_active: true})

    // Vars
    extra_class = extra_class || className || ""
    const m = side == "left" ? "mr-2" : "ml-2"

    function onClick() {
        // toggle the group state and pass "group" as the source,
        // so child elements can react accordingly
        setActive({group_active: !group_active, group_source: "group"})
    }

    ////////////////////////
    // Render
    return (

        <div className={m}>

            {name && <small className={`button_group_header ${extra_class} ${group_active ? "" : "disabled"}`} onClick={onClick}>{name}</small>}

            <div className="bg-dark p-1 rounded border align-items-start button_group">
                <ButtonGroupContext.Provider value={[{group_active, group_source}, setActive]}>
                {children}
                </ButtonGroupContext.Provider>
            </div>
        </div>
    )
}

