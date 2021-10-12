import React from 'react'
import { useDispatch } from 'react-redux'
import { set_filters } from '../../../store/ui.js'
import ButtonGroup from '../shared/ButtonGroup.jsx'
import DurationInputGroup from "../../shared/DurationInputGroup.jsx"


/**
 * Group to set the min/max killtime-filter
 *
 * @returns {ReactComponent}
 */
export default function FilterKilltimeGroup() {

    const dispatch = useDispatch()

    // Callback when values get changed
    function onChange({min, max}) {
        dispatch(set_filters({killtime: {min, max}}))
    }

    // Render
    return (
        <ButtonGroup name="Killtime 23" side="right">
            <DurationInputGroup onChange={onChange} className="input-group-sm killtime_input" />
        </ButtonGroup>
    )
}
