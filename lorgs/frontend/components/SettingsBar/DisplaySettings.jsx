

import React from 'react'
import { useSelector, useDispatch } from 'react-redux'
import ButtonGroup from './shared/ButtonGroup.jsx'
import { set_value, get_value } from '../../store/ui.js'


function Button({attr_name, icon_name, tooltip=""}) {

    const attr_value = useSelector(state => get_value(state, attr_name))
    const dispatch = useDispatch()
    const disabled = attr_value ? "" : "disabled"

    function onClick() {
        dispatch(set_value({
            field: attr_name,
            value: !attr_value,
        }))
    }

    return (
        <div
            className={`button icon-s rounded border-white ${icon_name} ${disabled}`}
            data-tip={tooltip}
            onClick={onClick}
        />
    )
}


export default function DisplaySettings() {
    
    return (
        <>
            <ButtonGroup name="Display" side="left">
                <Button attr_name="show_casticon" icon_name="fas fa-image" tooltip="spell icon" />
                <Button attr_name="show_casttime" icon_name="fas fa-clock" tooltip="cast time" />
                <Button attr_name="show_duration" icon_name="fas fa-stream" tooltip="duration" />
                <Button attr_name="show_cooldown" icon_name="fas fa-hourglass" tooltip="cooldown" />
            </ButtonGroup>
        </>
    )
}
