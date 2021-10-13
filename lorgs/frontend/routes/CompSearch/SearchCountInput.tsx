
import React from 'react'
import { useFormContext, useWatch  } from "react-hook-form";


/** options for the operator dropdown */
const OP_OPTIONS = (
    <>
    <option value="eq">=</option>
    <option value="lt">&lt;</option>
    <option value="gt">&gt;</option>
    <option value="lte">≤</option>
    <option value="gte">≥</option>
    </>
)

/**
 * Component to set a count-filter for a given attribute.
 * Allows the user to enter a number and a operator ("=", ">", "<", etc)
 *
 * @param {string} name attribute name this input should control
 * @param {string} icon_path path for the icon
 * @param {string} class_name name of a wow-class to use for border colors (uses `name` otherwise)
 *
 * @returns {ReactComponent}
 */
export default function CountFilterGroup({name, icon_path, class_name}) {

    // form attribute names
    const attr_name_count = name + ".count"
    const attr_name_op = name + ".op"

    // hooks
    const { register } = useFormContext();
    const value = useWatch({ name: attr_name_count });

    const active = value ? "" : "empty"

    return (
        <div className={`count-input-group wow-border-${class_name||name} ${active}`}>

            <img className="icon-s" src={icon_path}/>

            <select
                className="op-dropdown"
                {...register(attr_name_op)}
            >
                {OP_OPTIONS}
            </select>

            <input
                name={name}
                type="number"
                className="count-number text-center"
                placeholder="-" min="0"
                {...register(attr_name_count)}
            />
        </div>
    )
}
