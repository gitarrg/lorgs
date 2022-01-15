import FILTERS from "../../filter_logic";
import styles from "./PlayerName.scss"
import type Actor from "../../types/actor";
import type Fight from "../../types/fight";
import { FightInfo } from "./FightInfo";
import { useAppSelector } from "../../store/store_hooks";
import { PlayerName, BossName} from "./PlayerName"


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

    const filters = useAppSelector(state => state.ui.filters)
    const visible = FILTERS.is_fight_visible(fight, filters)
    if (!visible) { return null}

    return (
        <div className={styles.fight}>
            <div className={styles.names_container}>
                <FightInfo fight={fight} />
                {create_boss(fight)}
                {create_players(fight)}
            </div>
        </div>
    )
}
