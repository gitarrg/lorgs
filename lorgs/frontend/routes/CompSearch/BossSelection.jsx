/*
    Component to show the currently selected Boss
*/

import React from 'react'
import { useSelector } from 'react-redux'
import { useWatch } from "react-hook-form";


export default function BossSelection({}) {

    let header_content = <div className="text-muted">select a boss</div>

    const boss_name_slug = useWatch({name: "boss_name_slug"}) 
    const boss = useSelector(state => state.bosses.find(boss => boss.full_name_slug == boss_name_slug))

    if (boss) {
        const icon_path = `/static/images/bosses/sanctum-of-domination/${boss.full_name_slug}.jpg`
        header_content = <>
            <span className="wow-boss">{boss.name || boss.full_name}</span>
            <img className="icon-l rounded shadow wow-border-boss ml-2" src={icon_path} alt={boss.name}></img>
        </>
    }

    return <h1 className="m-0 ml-auto">{header_content}</h1>
}
