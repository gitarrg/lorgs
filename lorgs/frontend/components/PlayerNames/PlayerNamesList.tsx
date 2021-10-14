
import React from "react";
import { get_fights } from "../../store/fights";
import FILTERS from "../../filter_logic";

import {PlayerName, BossName} from "./PlayerName"
import Fight from "../../types/fight";
import Actor from "../../types/actor";
import { useAppSelector } from "../../store/store_hooks";


function create_boss(fight: Fight) {
    if (!(fight.boss?.name)) {return}
    return <BossName key="boss" fight={fight} boss={fight.boss} />
}


function create_player(fight: Fight, player: Actor) {
    return <PlayerName key={`${fight.report_id}_${player.name}`} fight={fight} player={player} />
}


function create_players(fight: Fight) {
    return fight.players.map(player => ( create_player(fight, player)))
}


export default function PlayerNamesList() {

    // get data
    const mode = useAppSelector(state => state.ui.mode)
    const fights = useAppSelector(state => get_fights(state))
    const filters = useAppSelector(state => state.ui.filters)

    ///////////////////
    // apply filters
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
