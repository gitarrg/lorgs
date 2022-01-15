

import { useState, useEffect, useContext } from 'react'
import WebpImg from '../../WebpImg'

import { ButtonGroupContext } from '../shared/ButtonGroup'


export default function FilterButton(
    {name, icon_name, full_name="", show_init=true, onClick} : {name: string, icon_name: string, full_name?: string, show_init?: boolean, onClick?: Function }) {

    // Hooks
    const [show, setShow] = useState(show_init)
    const group_context = useContext(ButtonGroupContext)

    full_name = full_name || name
    const icon_path = `/static/img/${icon_name}.jpg`
    const disabled = show ? "" : "disabled"

    function toggle_button() {
        const new_value = !show

        // update the state
        if (onClick) {
            onClick({value: new_value})
        }

        // update parent group
        if (new_value && group_context.setter) {
            group_context.setter({active: new_value, source: "child"})
        }

        // update the button itself
        setShow(new_value)
    }

    // see SpellButton,jsx
    useEffect(() => {
        if (group_context.source !== "group") { return}

        if (onClick) { onClick({value: group_context.active})}
        setShow(group_context.active)
    }, [group_context.active])


    /////////////////
    // Render
    return (
        <div data-tooltip={full_name}>
            <WebpImg
                className={`button icon-s rounded wow-border-${name} ${disabled}`}
                src={icon_path}
                alt={full_name}
                onClick={toggle_button}
            />
        </div>
    )
}
