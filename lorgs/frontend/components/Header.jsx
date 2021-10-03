
import React from 'react'
import { useSelector } from 'react-redux'
import { MODES } from "../data_store.js"


function get_header_spec_rankings(spec, boss) {
    if (!spec) { return null }
    if (!spec.class) { return null }

    const spec_name = spec.full_name + "s"
    const class_name = "wow-" + spec.class.name_slug

    return (
        <>
            <span className={class_name}>{spec_name}</span>
            <span> vs. </span>
            <span>{boss.full_name}</span>
        </>
    )
}


function get_header_comp_rankings(boss) {

    const boss_icon_path = `/static/images/bosses/sanctum-of-domination/${boss.full_name_slug}.jpg`
    return (
        <>
            <img className="icon-l rounded shadow border-white mr-2" src={boss_icon_path} alt={boss.name} target="_blank"></img>
            <span>{boss.full_name}</span>
        </>
    )
}


export default function Header() {

    const boss = useSelector(state => state.boss)
    const spec = useSelector(state => state.spec)
    const mode = useSelector(state => state.mode)

    let header_content = "loading..."
    switch (mode) {
        case MODES.SPEC_RANKING:
            header_content = get_header_spec_rankings(spec, boss) || header_content
            break;
        case MODES.COMP_RANKING:
            header_content = get_header_comp_rankings(boss)
        default:
            break;
    }

    return <h1 className="m-0">{header_content}</h1>
}
