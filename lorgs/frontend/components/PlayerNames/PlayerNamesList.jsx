
import React from "react";
import { useSelector } from 'react-redux'

import {PlayerName, BossName} from "./PlayerName.jsx"


function create_boss(fight) {
    if (!(fight.boss && fight.boss.name)) {return}
    if (fight.boss.visible === false) { return }
    return <BossName key="boss" fight={fight} boss={fight.boss} />
}


function create_player(fight, player) {
    if (player.visible === false) { return }
    return <PlayerName key={`${fight.report_id}_${player.name}`} fight={fight} player={player} />
}


function create_players(fight) {
    return fight.players.map(player => ( create_player(fight, player)))
}


function create_fight(i, fight) {
    if (fight.visible === false) { return }

    return (
        <div key={`fight_${i}`} className="player_names_fight">
            {create_boss(fight)}
            {create_players(fight)}
        </div>
    )
}


export default function PlayerNamesList() {

    // get data
    const mode = useSelector(state => state.mode)
    const fights = useSelector(state => state.fights)

    // include this as it affects the display for the fights
    const filters = useSelector(state => state.filters)

    // render
    return (
        <div className={`player_names_container ${mode}`}>
            {
                fights.map((fight, i) => (
                    create_fight(i, fight)
                ))
            }
        </div>
    )
}
