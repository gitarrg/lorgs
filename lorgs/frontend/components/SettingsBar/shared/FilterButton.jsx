


import React from 'react'


export default function FilterButton({name, icon_name, full_name="", show_init=true, onClick=null}) {

    const [show, setShow] = React.useState(show_init)

    full_name = full_name || name
    const icon_path = `/static/images/${icon_name}.jpg`

    function toggle_button() {

        // console.log("clicked", name, show)
        // update the context
        // context.filters = {...context.filters}  // create new object
        // context.filters[covenant_slug] = !show
        // context.refresh()

        // update the state
        if (onClick) {
            onClick({value: !show})
        }

        setShow(!show)
    }

    return (
        <img 
            className={`button icon-s rounded wow-border-${name} ${!show && "disabled"}`}
            src={icon_path}
            data-bs-toggle="tooltip"
            title={full_name}
            alt={full_name}
            onClick={toggle_button}
        />
    )
}
