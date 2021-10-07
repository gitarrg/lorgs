/*
    Component to show the currently selected Roles/Specs
*/

import React from 'react'
import { useWatch } from "react-hook-form";

// convert "eq", "lt", "gt" etc to "<", ">""
function op_to_symbol(op) {

    if (op == "eq") {return ""}
    if (op == "lt") {return "<"}
    if (op == "gt") {return ">"}
    if (op == "lte") {return "≤"}
    if (op == "gte") {return "≥"}
    console.warn("unknown op:", op)
    return ""
}


function create_icon(prefix, name, count, op) {

    if (count === "") {return}

    // special case for excludes
    const excluded = (op === "eq") && (count === "0")

    const icon_path = `/static/images/${prefix}/${name}.jpg`
    const label = `${op_to_symbol(op)}${count}`
    const class_name = name.split("-")[0]

    return (
        <div key={name} className={`player-selection__icon ${excluded ? "excluded" : ""}`}>

            <div className={`player-selection__icon__img rounded wow-border-${class_name}`}>
                <img className="icon-l" src={icon_path}/>
            </div>

            {!excluded && <div className={`player-selection__label wow-${class_name}`}>{label}</div>}
            {excluded && <div className="player-selection__label">X</div>}
        </div>
    )
}


function create_icons(prefix, items) {

    let icons = []
    for (const [key, value] of Object.entries(items)) {

        const icon = create_icon(prefix, key, value.count, value.op)
        if (icon) {
            icons.push(icon)
        }
    }
    return icons
}


export default function PlayerSelection({}) {

    // Fetch Form Vars
    const roles = useWatch({name: "role"})
    const specs = useWatch({name: "spec"})

    // Build Content
    let header_content = []
    if (roles) {
        header_content.push(...create_icons("roles", roles))
    }
    if (specs) {
        header_content.push(...create_icons("specs", specs))
    }
    header_content = header_content.length > 0  ? header_content : "any comp"

    // Return
    return <h1 className="m-0 mr-auto d-flex" style={{gap: "0.5rem"}}>{header_content}</h1>
}
