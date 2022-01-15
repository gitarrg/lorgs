import Icon from '../../shared/Icon'
import style from "./CollapsableSpellGroup.scss"
import type Boss from "../../../types/boss"
import type Class from "../../../types/class"
import type Spec from "../../../types/spec"
import { ReactNode, useState } from 'react'


type CollapsableSpellGroupProps = {

    /** Element used for the Icon, Label and Color */
    spec: Spec|Boss|Class

    /** The chilren inside the group */
    children: ReactNode

}


export default function CollapsableSpellGroup({spec, children} : CollapsableSpellGroupProps) {

    // Hooks
    const [collapsed, setCollapsed] = useState(false)

    function onClick() {
        setCollapsed(!collapsed)
    }

    // @ts-ignore
    const wow_class = spec.code ?? spec.class?.name_slug ?? spec.name_slug

    /////////////////////////////////////
    // Render
    return <>
        <div className={`${style.group} wow-${wow_class}`}>

            <div onClick={onClick}>
                <Icon spec={spec} className={`${style.button} ${collapsed ? "closed" : "open"} button grow-when-touched`}/>
            </div>

            {!collapsed && <div className={`${style.children} `}>
                {children}
            </div>
            }
        </div>
    </>
}
