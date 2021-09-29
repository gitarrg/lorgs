
import React, { useState, useEffect } from "react";
import PlayerName from "./PlayerName.jsx"


export default function PlayerNamesList(props) {

    return (
        <div id="player_names_container" className="player_names_container spec_ranking">

            {props.players.map(player => (
                <PlayerName key={player.name} player={player} />
            ))}

        </div>

    )
}
