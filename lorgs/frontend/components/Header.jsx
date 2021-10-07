
import React from 'react'
import { useSelector } from 'react-redux'
import { WCL_URL } from '../constants.js'
import { MODES } from "../data_store.js"



function get_spec_ranking_url(spec, boss) {

    const metric = spec.role == "heal" ? "hps" : "dps"

    let url = new URL(WCL_URL)
    url.pathname = "/zone/rankings/28"
    url.hash = new URLSearchParams({
        boss: boss.id,
        class: spec.class.name,
        spec: spec.name,
        metric: metric,
    })
    return url


}

function get_header_spec_rankings(spec, boss) {
    if (!spec) { return null }
    if (!spec.class) { return null }

    const spec_name = spec.full_name + "s"
    const class_name = "wow-" + spec.class.name_slug

    const url = get_spec_ranking_url(spec, boss)
    
    // `${WCL_URL}/zone/rankings/28#boss=2423&class=Druid&spec=Restoration&metric=hps`

    return (
        <a href={url} target="_blank">
            <span className="wow-boss">{boss.full_name}</span>
            <span> vs. </span>
            <span className={class_name}>{spec_name}</span>
        </a>
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
