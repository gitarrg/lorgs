

import React from 'react'
import { useSelector, useDispatch } from 'react-redux'
import ButtonGroup, { ButtonGroupContext } from './shared/ButtonGroup.jsx'
import { update_settings } from '../../store/ui.js'


function Button({attr_name, icon_name, tooltip=""}) {

    ////////////////////////
    // Hooks
    //
    const attr_value = useSelector(state => state.ui.settings[attr_name])
    const dispatch = useDispatch()
    const disabled = attr_value ? "" : "disabled"
    const [{group_active, group_source}, set_group_active] = React.useContext(ButtonGroupContext)


    function onClick() {
        const new_value = !attr_value

        dispatch(update_settings({
            [attr_name]: new_value
        }))

        if (new_value) {
            set_group_active({group_active: new_value, group_source: "child"})
        }
    }

    // see SpellButton,jsx
    React.useEffect(() => {
        if (group_source !== "group") { return}
        dispatch(update_settings({
            [attr_name]: group_active
        }))
    }, [group_active])

    ////////////////////////
    // Render
    //
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
