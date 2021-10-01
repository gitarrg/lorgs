

import React from 'react'
import ButtonGroup from './shared/ButtonGroup.jsx'
import AppDataContext from "./../../AppDataContext.jsx"



export default function DisplaySettings() {
    
    const shared_classes = "button icon-s rounded border-white"
    
    const context = React.useContext(AppDataContext)


    function toggle_attr(attr_name) {
            function toggler() {
                let new_context = {...context}
                new_context[attr_name] = !new_context[attr_name]
                context.setContext(new_context)
            }
        return toggler
    }


    return (
        <>
            <ButtonGroup name="Display">
                <div onClick={toggle_attr("show_casttime")} className={`${shared_classes} ${!context.show_casttime && "disabled"} fas fa-clock`} data-bs-toggle="tooltip" title="cast time" />
                <div onClick={toggle_attr("show_duration")} className={`${shared_classes} ${!context.show_duration && "disabled"} fas fa-stream `} data-bs-toggle="tooltip" title="duration" />
                <div onClick={toggle_attr("show_cooldown")} className={`${shared_classes} ${!context.show_cooldown && "disabled"} fas fa-hourglass `} data-bs-toggle="tooltip" title="cooldown" />
            </ButtonGroup>
        </>
    )
}
