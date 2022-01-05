import { createContext, ReactNode, useState } from 'react'
import styles from "./ButtonGroup.scss"


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


type ButtonGroupProps = {

    name?: string,
    extra_class?: string,
    className?: string,
    children?: ReactNode
}

export default function ButtonGroup({name, extra_class, className, children} : ButtonGroupProps) {
    ///////////////////////
    // Hooks

    // The Groups Active state:
    // in addition to the "group_active"-value, we pass a "group_source",
    // which can be used to determine who changed the groups state.
    const [{active, source}, setActive] = useState({active: true, source: ""})
    const group_context : ButtonGroupContextType = {active, source, setter: setActive}

    // Vars
    extra_class = extra_class || className || ""

    function onClick() {
        // toggle the group state and pass "group" as the source,
        // so child elements can react accordingly
        setActive({active: !active, source: "group"})
    }

    ////////////////////////
    // Render
    return (
        <div>
            {name && <small className={`${styles.header} ${extra_class} ${active ? "" : "disabled"}`} onClick={onClick}>{name}</small>}
            <div className="d-flex">  {/* wraper to shrink the child div */}
                <div className={`${styles.group} bg-dark p-1 rounded border`}>
                    <ButtonGroupContext.Provider value={group_context}>
                    {children}
                    </ButtonGroupContext.Provider>
                </div>
            </div>
        </div>
    )
}

