

import React from 'react'
import { useSelector } from 'react-redux'
import ButtonGroup from './shared/ButtonGroup.jsx'
import data_store from '../../data_store.js'


function Button({attr_name, icon_name}) {

    const attr_value = useSelector(state => state[attr_name])
    
    function onClick() {
        data_store.dispatch({
            type: "update_value",
            field: attr_name,
            value: !attr_value,
        })
    }

    return (
        <div
            className={`button icon-s rounded border-white ${icon_name} ${!attr_value && "disabled"}`}
            onClick={onClick}
        />
    )
}


export default function DisplaySettings() {
    
    return (
        <>
            <ButtonGroup name="Display" side="left">
                <Button attr_name="show_casttime" icon_name="fas fa-clock" data-bs-toggle="tooltip" title="cast time" />
                <Button attr_name="show_duration" icon_name="fas fa-stream"  data-bs-toggle="tooltip" title="duration" />
                <Button attr_name="show_cooldown" icon_name="fas fa-hourglass"  data-bs-toggle="tooltip" title="cooldown" />
            </ButtonGroup>
        </>
    )
}
