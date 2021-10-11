

import React from 'react'


export default function FilterButton({name, icon_name, full_name="", show_init=true, onClick=null}) {

    const [show, setShow] = React.useState(show_init)

    full_name = full_name || name
    const icon_path = `/static/images/${icon_name}.jpg`
    const disabled = show ? "" : "disabled"

    function toggle_button() {

        // update the state
        if (onClick) {
            onClick({value: !show})
        }
        setShow(!show)
    }

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
