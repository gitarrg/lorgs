import {PlayerName, BossName} from "./PlayerName"
import type Fight from "../../types/fight";
import type Actor from "../../types/actor";
import { FightInfo } from "./FightInfo";

// @ts-ignore
import styles from "./PlayerName.scss"


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



export default function PlayerNamesFight( {i, fight} : {i: number, fight: Fight} ) {

    return (
        <div className={styles.fight}>
            <FightInfo fight={fight} />

            <div className={styles.names_container}>
                {create_boss(fight)}
                {create_players(fight)}
            </div>
        </div>
    )
}
