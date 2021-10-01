import React from 'react'

import AppDataContext from "./../../../AppDataContext.jsx"



export default function FilterCovenant(props) {

    const [show, setShow] = React.useState(true)
    const context = React.useContext(AppDataContext)

    const covenant_slug = props.covenant.toLowerCase()
    const icon_path = `/static/images/covenants/${covenant_slug}.jpg`
    const disabled = !show && "disabled"


    function toggle_button() {
        // update the context
        context.filters = {...context.filters}  // create new object
        context.filters[covenant_slug] = !show
        context.setContext({...context})

        // update the state
        setShow(!show)
    }

    return (
        <img 
            className={`button icon-s rounded wow-border-${covenant_slug} ${disabled}`}
            src={icon_path}
            data-bs-toggle="tooltip"
            title={props.covenant}
            alt={props.covenant}
            onClick={toggle_button}
        />
    )
}
