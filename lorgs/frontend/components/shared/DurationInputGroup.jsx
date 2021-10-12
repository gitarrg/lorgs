import React from 'react'
import DurationInput from "./DurationInput.jsx";

/**
    A Group of two duration inputs separated by a dash.
    This can be used as a standard min/max duration input.

    @param {function} onChange Function, which will be called, with an object
        containing a "min" and "max" integer for the
        respective value of seconds.

    @param {string} placeholder_min placeholder for the min-value
    @param {string} placeholder_max placeholder for the max-value
    @param {string} className additional class to apply to the parent group

    @returns {ReactComponent} <div>
*/
export default function DurationInputGroup({
    onChange,
    placeholder_min="0:00",
    placeholder_max="0:00",
    className="",
}) {

    /////////////////////////
    // State
    const [value_min, set_value_min] = React.useState(0)
    const [value_max, set_value_max] = React.useState(0)

    /////////////////////////
    // pass values to callback
    React.useEffect(() => {
        onChange && onChange({min: value_min, max: value_max})
    }, [value_min, value_max])

    /////////////////////////
    // Render
    // todo: if size == small "form-control-sm"
    const is_empty = value_min === undefined && value_max == undefined

    return (
        <div className={`duration_input__group input-group ${className} ${is_empty ? "empty" : ""}`}>
            <DurationInput name="min" onChange={set_value_min} placeholder={placeholder_min}/>
            <span className="duration_input__dash input-group-text">-</span>
            <DurationInput name="max" onChange={set_value_max} placeholder={placeholder_max} />
        </div>
    )
}
