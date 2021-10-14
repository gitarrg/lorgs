import { createContext, useState } from 'react'


type ButtonGroupContextType = {
    /** If the group itself is active or not. */
    active: boolean

    /** Type of element that triggered a change. */
    source: string //"group" | "child" | ""

    /** Callable to change the Group Context. Expects active and source keys*/
    setter?: Function
}


const DEFAULT_CONTEXT: ButtonGroupContextType = {
    active: true,
    source: "",
}


export const ButtonGroupContext = createContext<ButtonGroupContextType>(DEFAULT_CONTEXT)


export default function ButtonGroup(
    {name, extra_class, className, side="left", children} :
    {name: string, extra_class?: string, className?: string, side?: "left"|"right", children?: JSX.Element[] | JSX.Element }
    ) {

    ///////////////////////
    // Hooks

    // The Groups Active state:
    // in addition to the "group_active"-value, we pass a "group_source",
    // which can be used to determine who changed the groups state.
    const [{active, source}, setActive] = useState({active: true, source: ""})
    const group_context : ButtonGroupContextType = {active, source, setter: setActive}

    // Vars
    extra_class = extra_class || className || ""
    const m = side == "left" ? "mr-2" : "ml-2"

    function onClick() {
        // toggle the group state and pass "group" as the source,
        // so child elements can react accordingly
        setActive({active: !active, source: "group"})
    }

    ////////////////////////
    // Render
    return (

        <div className={m}>

            {name && <small className={`button_group_header ${extra_class} ${active ? "" : "disabled"}`} onClick={onClick}>{name}</small>}

            <div className="bg-dark p-1 rounded border align-items-start button_group">
                <ButtonGroupContext.Provider value={group_context}>
                {children}
                </ButtonGroupContext.Provider>
            </div>
        </div>
    )
}

