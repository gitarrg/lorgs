
import React, { useState, useEffect } from "react";
import PlayerName from "./PlayerName.jsx"
import AppDataContext from "./../AppDataContext.jsx"


export default function PlayerNamesList(props) {

    const ctx = React.useContext(AppDataContext)

    return (

        <React.Fragment>

            {ctx.fights.map((fight, f) => (

                <div key={`fight_${f}`} id="player_names_container" className="player_names_container spec_ranking">
                    {fight.players.map((player, p) => (
                        <PlayerName key={`player_${p}`} fight={player.fight || fight} player={player} />
                    ))}
                </div>
            ))}

        </React.Fragment>
    )
}
