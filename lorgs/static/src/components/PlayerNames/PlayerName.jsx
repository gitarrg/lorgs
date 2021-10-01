
import React  from "react";


function spec_ranking_color(i = 0) {

    if (i == -1) { return "" } else
    if (i == 1) { return "text-artifact" } else
    if (i <= 25) { return "text-astounding" } else
    if (i <= 100) { return "text-legendary" } else { return "epic" }
}


const SKELETON_PLAYER_NAME = (
    <div className="loading player_name">
        <img className="player_name__spec_icon"></img>
        <span className="player_name__rank">loading...</span>
    </div>
)


export function BossName(props) {

    const boss = props.boss;
    const img_path = `/static/images/bosses/sanctum-of-domination/${boss.name_slug}.jpg`

    if (props.fight.loading) { return SKELETON_PLAYER_NAME }

    return (
        <div className="boss_name">
            <a target="_blank" href={props.fight.report_url}>
                <img className="boss_name__spec_icon" src={img_path}></img>
                <span className="boss_name__name">{boss.name}</span>
            </a>
        </div>
    )
}


export function PlayerName(props) {

    // console.log(props, props.player)
    const player = props.player;
    const fight = player.fight || props.fight;
    let img_path = player.spec_slug && `/static/images/specs/${player.spec_slug}.jpg`
    img_path = `/static/images/covenants/${player.covenant}.jpg`

    if (fight.loading) { return SKELETON_PLAYER_NAME }

    return (
        <div className={"player_name " + spec_ranking_color(player.rank)}>

            <a target="_blank" href={fight.report_url}>
                <img className="player_name__spec_icon" src={img_path}></img>
                <span className={`player_name__name wow-${player.class_slug}`}>{player.name}</span>
                {player.rank > 0 && <span className="player_name__rank">#{player.rank}</span>}
                {player.total && <span className="player_name__total">{kFormatter(player.total)}</span>}
            </a>
        </div>
    )
}
