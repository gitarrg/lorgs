

import React from 'react'

import { ButtonGroupContext } from '../shared/ButtonGroup'


export default function FilterButton({name, icon_name, full_name="", show_init=true, onClick=null}) {

    // Hooks
    const [show, setShow] = React.useState(show_init)
    const [{group_active, group_source}, set_group_active] = React.useContext(ButtonGroupContext)

    full_name = full_name || name
    const icon_path = `/static/images/${icon_name}.jpg`
    const disabled = show ? "" : "disabled"

    function toggle_button() {
        const new_value = !show

        // update the state
        if (onClick) {
            onClick({value: new_value})
        }
        // update parent group
        if (new_value) {
            set_group_active({group_active: new_value, group_source: "child"})
        }

        // update the button itself
        setShow(new_value)
    }

    // see SpellButton,jsx
    React.useEffect(() => {
        if (group_source !== "group") { return}

        onClick({value: group_active})
        setShow(group_active)
    }, [group_active])


    /////////////////
    // Render
    return (
        <div data-tooltip={full_name}>
            <img
                className={`button icon-s rounded wow-border-${name} ${disabled}`}
                src={icon_path}
                alt={full_name}
                onClick={toggle_button}
            />
        </div>
    )
}
