

import React from 'react'
import { useSelector, useDispatch } from 'react-redux'
import ButtonGroup from './shared/ButtonGroup.jsx'
import { update_settings } from '../../store/ui.js'


function Button({attr_name, icon_name, tooltip=""}) {

    const attr_value = useSelector(state => state.ui.settings[attr_name])
    const dispatch = useDispatch()
    const disabled = attr_value ? "" : "disabled"

    function onClick() {
        dispatch(update_settings({
            [attr_name]: !attr_value
        }))
    }

    return (
        <div data-tooltip={tooltip}>
            <div
                className={`button icon-s rounded border-white ${icon_name} ${disabled}`}
                onClick={onClick}
            />
        </div>
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
