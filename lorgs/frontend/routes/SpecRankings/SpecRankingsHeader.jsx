
import React from 'react'
import { useSelector } from 'react-redux'

import HeaderLogo from './../../components/HeaderLogo.jsx'
import { WCL_URL } from '../../constants.js'
import { get_boss } from '../../store/bosses.js'
import { get_spec } from '../../store/specs.js'


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


export default function SpecRankingsHeader({spec_slug, boss_slug}) {

    // hoosk
    const spec = useSelector(state => get_spec(state, spec_slug))
    const boss = useSelector(state => get_boss(state, boss_slug))
    if (!spec || !boss) { return null }


    // prep vars
    const spec_name = spec.full_name + "s"
    const class_name = "wow-" + spec.class.name_slug
    const url = get_spec_ranking_url(spec, boss)

    // Render
    return (
        <h1 className="m-0 d-flex align-items-center">
            <HeaderLogo wow_class={class_name} />
            <a href={url} target="_blank">
                <span className="wow-boss wow-text ml-2">{boss.full_name}</span>
                <span>&nbsp;vs.&nbsp;</span>
                <span className={class_name}>{spec_name}</span>
            </a>
        </h1>
    )
}
