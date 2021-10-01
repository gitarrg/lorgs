import React from 'react'

import AppContext from "./../../../AppContext/AppContext.jsx"



export default function FilterCovenant({covenant}) {

    const covenant_slug = covenant.toLowerCase()

    const context = AppContext.getData()
    const [show, setShow] = React.useState(context.filters[covenant_slug] !== false)

    const icon_path = `/static/images/covenants/${covenant_slug}.jpg`

    function toggle_button() {
        // update the context
        context.filters = {...context.filters}  // create new object
        context.filters[covenant_slug] = !show
        context.refresh()

        // update the state
        setShow(!show)
    }

    return (
        <img 
            className={`button icon-s rounded wow-border-${covenant_slug} ${!show && "disabled"}`}
            src={icon_path}
            data-bs-toggle="tooltip"
            title={covenant}
            alt={covenant}
            onClick={toggle_button}
        />
    )
}
