import FightWidget from "./FightWidget"
import styles from "./FightSelectList.scss"
import { get_user_report_fights } from '../../store/user_reports'
import { useAppSelector } from '../../store/store_hooks'

export default function FightSelectList() {

    // Hooks
    const fights = useAppSelector(state => get_user_report_fights(state))

    // render
    return (
        <div className={styles.container}>
            {fights.map(fight =>
                <FightWidget key={fight.fight_id} fight={fight} />
            )}
        </div>
    )
}
