
import React from 'react'
import { useFormContext } from "react-hook-form";

import DurationInputGroup from '../../components/shared/DurationInputGroup.jsx'
import FormGroup from './FormGroup.jsx'


/**
 * Component to input a min/max-killtime
 *
 * @returns {ReactComponent}
 */
export default function KilltimeGroup() {

    const form_methods = useFormContext();

    // state to set and receive the values
    const [values, set_values] = React.useState({min: 0, max: 0})

    // Pass values to form
    React.useEffect(() => {
        form_methods.setValue("killtime_min", values.min)
        form_methods.setValue("killtime_max", values.max)

    }, [values])
    console.log("values", values)

    ////////////////////////////
    // Render
    return (
        <FormGroup name="Killtime:" className="killtime-search">
            <DurationInputGroup onChange={set_values}/>
        </FormGroup>
    )
}
