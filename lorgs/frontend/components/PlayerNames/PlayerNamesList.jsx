
import React from "react";
import { useSelector } from 'react-redux'
import { get_fights } from "../../store/fights.js";
import FILTERS from "../../filter_logic.js";

import {PlayerName, BossName} from "./PlayerName.jsx"


function create_boss(fight) {
    if (!(fight.boss && fight.boss.name)) {return}
    return <BossName key="boss" fight={fight} boss={fight.boss} />
}


function create_player(fight, player) {
    return <PlayerName key={`${fight.report_id}_${player.name}`} fight={fight} player={player} />
}


function create_players(fight) {
    return fight.players.map(player => ( create_player(fight, player)))
}



export default function PlayerNamesList() {

    // get data
    const mode = useSelector(state => state.ui.mode)
    const fights = useSelector(state => get_fights(state))
    const filters = useSelector(state => state.ui.filters)

    ///////////////////
    // apply filters
    // if (!fight) { return null}
    // if (!FILTERS.is_fight_visible(fight, filters)) { return null}
    const visible_fights = fights.filter(fight => FILTERS.is_fight_visible(fight, filters))

    ///////////////////
    // render
    return (
        <div className={`player_names_container ${mode}`}>
            {visible_fights.map((fight, i) => (
                <div key={`fight_${i}`} className="player_names_fight">
                    {create_boss(fight)}
                    {create_players(fight)}
                </div>
            ))}
        </div>
    )
}
