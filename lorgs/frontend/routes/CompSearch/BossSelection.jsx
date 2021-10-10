/*
    Component to show the currently selected Boss
*/

import React from 'react'
import { useSelector } from 'react-redux'
import { useWatch } from "react-hook-form";

import { get_boss } from '../../store/bosses.js';


export default function BossSelection() {

    let header_content = <div className="text-muted">select a boss</div>

    // currently selected boss name
    const boss_name_slug = useWatch({name: "boss_name_slug"}) 
    const boss = useSelector(state => get_boss(state, boss_name_slug))


    if (boss && boss.full_name) {
        header_content = <>
            <span className="wow-boss">{boss.full_name}</span>
            <img className="icon-l rounded shadow wow-border-boss ml-2" src={boss.icon_path} alt={boss.name}></img>
        </>
    }

    return <h1 className="m-0 ml-auto">{header_content}</h1>
}
