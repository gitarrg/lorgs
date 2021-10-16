import FILTERS from "../../filter_logic";
import PlayerNamesFight from "./PlayerNamesFight";
import { get_fights } from "../../store/fights";
import { useAppSelector } from "../../store/store_hooks";


export default function PlayerNamesList() {

    // get data
    const fights = useAppSelector(state => get_fights(state))
    const filters = useAppSelector(state => state.ui.filters)

    ///////////////////
    // apply filters
    const visible_fights = fights.filter(fight => FILTERS.is_fight_visible(fight, filters))  // TODO: add to fight-slice

    ///////////////////
    // render
    return (
        <div>
            {visible_fights.map((fight, i) => (
                <PlayerNamesFight key={i} fight={fight} i={i}/>
            ))}
        </div>
    )
}
