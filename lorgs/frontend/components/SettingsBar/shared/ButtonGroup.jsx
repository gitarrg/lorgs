

import React from 'react'

export default function ButtonGroup(props) {

    const extra_class = props.extra_class || props.className || ""
    const m = props.side == "left" ? "mr-2" : "ml-2"

    return (

        <div className={m}>

            {props.name && <small className={extra_class}>{props.name}</small>}
            <div className="bg-dark p-1 rounded border align-items-start button_group">
                {props.children}
            </div>
        </div>
    )
}

