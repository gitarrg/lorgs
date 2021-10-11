/*
    Component to display a comp or comp-search.
    >>> eg.: 2x Tank, 4+ Healers, max 2x Holy Paladin

    Used for the CompSearch and CompRankings.

*/

import React from 'react'


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
        <div key={name} className={`comp-preview__icon rounded border-mid wow-${class_name} wow-border ${excluded ? "excluded" : ""}`}>
            <img className="icon-l" src={icon_path}/>
            {!excluded && <div className={`comp-preview__label wow-${class_name}`}>{label}</div>}
            {excluded && <div className="comp-preview__label">X</div>}
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


export default function CompPreview({roles={}, specs={}, placeholder=""}) {

    let icons = []
    icons.push(...create_icons("roles", roles))
    icons.push(...create_icons("specs", specs))

    return (
        <div className="comp-preview">
            {icons.length > 0 ? icons : placeholder}
        </div>
    )
}
