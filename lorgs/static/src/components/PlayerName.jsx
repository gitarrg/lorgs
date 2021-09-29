
import React, { useState, useEffect } from "react";

import AppDataContext from "./../AppDataContext.jsx"

function spec_ranking_color(i = 0) {

    if (i == 1) { return "text-artifact" } else
    if (i <= 25) { return "text-astounding" } else
    if (i <= 100) { return "text-legendary" } else { return "epic" }
}


export default function PlayerName(props) {

    // console.log(props, props.player)
    const player = props.player;
    const fight = player.fight || props.fight;
    const img_path = `/static/images/specs/${player.spec_slug}.jpg`

    return (
        <div className={"player_name " + spec_ranking_color(player.rank)}>

            <a target="_blank" href={fight.report_url}>

                <img className="player_name__spec_icon" src={img_path}></img>
                <span className={`player_name__name wow-${player.class_slug}`}>{player.name}</span>
                <span className="player_name__rank">#{player.rank}</span>
                <span className="player_name__total">{kFormatter(player.total)}</span>
            </a>

        </div>
    )
}
