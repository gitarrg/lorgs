
import React from "react";

import AppDataContext from "./../../AppDataContext.jsx"
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
        <React.Fragment key={`fight_${i}`}>
            {create_boss(fight)}
            {create_players(fight)}
        </React.Fragment>
    )
}



export default function PlayerNamesList() {

    const ctx = React.useContext(AppDataContext)


/*     <PlayerName key={`boss_${f}`} fight={fight} player={fight.boss} />

    fight.players.filter(player => player.visible).map((player, p) => (
        <PlayerName key={`player_${p}`} fight={fight} player={player} />
    )) */

    return (

        <div id="player_names_container" className="player_names_container spec_ranking">
            {
                ctx.fights.map((fight, i) => (
                    create_fight(i, fight)
                ))
            }
        </div>
    )
}
