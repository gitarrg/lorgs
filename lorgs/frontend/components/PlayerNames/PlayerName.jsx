
import React  from "react";
import AppContext from "./../../AppContext/AppContext.jsx"


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
    if (props.fight.loading) { return SKELETON_PLAYER_NAME }

    const boss = props.boss;
    const img_path = `/static/images/bosses/sanctum-of-domination/${boss.full_name_slug}.jpg`

    return (
        <div className="boss_name">
            <a target="_blank" href={props.fight.report_url}>
                <img className="boss_name__spec_icon" src={img_path}></img>
                <span className="boss_name__name">{boss.name}</span>
            </a>
        </div>
    )
}


export function PlayerName({player, fight}) {

    const context = AppContext.getData()

    // console.log(props, props.player)
    let spec_img_path = player.spec && `/static/images/specs/${player.spec}.jpg`
    let role_img_path = player.spec && `/static/images/roles/${player.role}.jpg`
    // img_path = `/static/images/covenants/${player.covenant}.jpg`

    const mode_spec = context.mode == AppContext.MODES.SPEC_RANKING
    const mode_comp = context.mode == AppContext.MODES.COMP_RANKING

    if (fight.loading) { return SKELETON_PLAYER_NAME }

    return (
        <div className={"player_name " + spec_ranking_color(player.rank)}>

            <a target="_blank" href={fight.report_url}>
                {mode_comp && <img className="player_name__role_icon" src={role_img_path}></img>}
                <img className="player_name__spec_icon" src={spec_img_path}></img>

                <span className={`player_name__name wow-${player.class}`}>{player.name}</span>
                {mode_spec && player.rank && <span className="player_name__rank">#{player.rank}</span>}
                {mode_spec && player.rank && player.total && <span className="player_name__total">{kFormatter(player.total)}</span>}
            </a>
        </div>
    )
}
