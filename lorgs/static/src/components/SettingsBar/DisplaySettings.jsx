

import React from 'react'
import ButtonGroup from './shared/ButtonGroup.jsx'
import AppContext from "./../../AppContext/AppContext.jsx"



export default function DisplaySettings() {
    
    const shared_classes = "button icon-s rounded border-white"
    
    const context = AppContext.getData()

    function toggle_attr(attr_name) {
        function toggler() {
            context[attr_name] = !context[attr_name]
            context.refresh()
        }
    return toggler
    }


    return (
        <>
            <ButtonGroup name="Display" side="left">
                <div onClick={toggle_attr("show_casttime")} className={`${shared_classes} ${!context.show_casttime && "disabled"} fas fa-clock`} data-bs-toggle="tooltip" title="cast time" />
                <div onClick={toggle_attr("show_duration")} className={`${shared_classes} ${!context.show_duration && "disabled"} fas fa-stream `} data-bs-toggle="tooltip" title="duration" />
                <div onClick={toggle_attr("show_cooldown")} className={`${shared_classes} ${!context.show_cooldown && "disabled"} fas fa-hourglass `} data-bs-toggle="tooltip" title="cooldown" />
            </ButtonGroup>
        </>
    )
}
