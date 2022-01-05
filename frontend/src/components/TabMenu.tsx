
import {
    cloneElement,
    createContext,
    ReactElement,
    ReactNode,
    useContext,
    useState,
} from "react";
import styles from "./TabMenu.scss"


type TabGroupContextType = {
    /** If the group itself is active or not. */
    active_tabs: {[key: number]: boolean}

    /** Callable to change the Group Context. Expects active and source keys*/
    setter?: Function
}


const DEFAULT_CONTEXT = {
    // tab: 0  should be shown by default
    active_tabs: {0: true}
}


const TabGroupContext = createContext<TabGroupContextType>(DEFAULT_CONTEXT)


export function TabTitle({index, children} : {index: number, children : ReactNode[]}) {

    const context = useContext(TabGroupContext)
    const selected = context.active_tabs[index]

    function onClick() {
        context.active_tabs = {}  // hide all other tabs
        context.active_tabs[index] = !selected
        context.setter && context.setter({...context})
    }

    return (
        <div className={`${styles.title} ${selected ? "selected" : ""}`} onClick={onClick}>
            {children}
        </div>
    )
}


export function Tab({index, icon, children} : {index?: number, title: ReactNode, icon?: ReactNode, children : ReactNode}) {

    const context = useContext(TabGroupContext)
    const selected = context.active_tabs[index || 0]

    if (!selected) { return null }
    return <>{children}</>
}


/** a sub-group of Tabs */
export function TabGroup({children, initial_tab=0} : {children : ReactElement[], initial_tab?: number}) {


    const initial_state = {...DEFAULT_CONTEXT, active_tabs: {[initial_tab]: true}}
    const [context, setContext] = useState<TabGroupContextType>(initial_state)
    context.setter = setContext

    return (
        <div>
            <TabGroupContext.Provider value={context}>

                <div className="d-flex gap-2">
                    {children.map((child, i) =>
                        <TabTitle key={i} index={i}>
                            {child.props.icon}
                            {child.props.title}
                        </TabTitle>
                    )}
                </div>

                <div className="d-flex gap-2">
                    {children.map((child, i) =>
                        cloneElement(child, {key: i, index: i})
                    )}
                </div>
            </TabGroupContext.Provider>
        </div>
    )
}


export function TabMenu({children} : {children : ReactNode}) {

    return (
        <div className={styles.menu}>
            {children}
        </div>
    );
}

