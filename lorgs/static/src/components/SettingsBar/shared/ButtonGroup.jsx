

import React from 'react'

export default function ButtonGroup(props) {

    const extra_class = props.extra_class || ""

    return (

        <div className="mr-2">

            {props.name && <small className={"clear-both " + extra_class}>{props.name}</small>}

            <div className="bg-dark p-1 rounded border">
                {props.children}
            </div>
        </div>
    )
}

