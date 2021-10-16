import {useState, useEffect } from 'react'
import DurationInput from "./DurationInput";
import styles from "./DurationInput.scss"


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
} : {onChange?: Function, placeholder_min?: string, placeholder_max?: string, className?: string}
) {

    /////////////////////////
    // State
    const [value_min, set_value_min] = useState(0)
    const [value_max, set_value_max] = useState(0)

    /////////////////////////
    // pass values to callback
    useEffect(() => {
        onChange && onChange({min: value_min, max: value_max})
    }, [value_min, value_max])

    /////////////////////////
    // Render
    // todo: if size == small "form-control-sm"
    const is_empty = value_min === undefined && value_max == undefined

    return (
        <div className={`duration_input__group input-group ${className} ${is_empty ? "empty" : ""}`}>
            <DurationInput onChange={set_value_min} placeholder={placeholder_min}/>
            <span className={`${styles.duration_input__dash} input-group-text`}>-</span>
            <DurationInput onChange={set_value_max} placeholder={placeholder_max} />
        </div>
    )
}
