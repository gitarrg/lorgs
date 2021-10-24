import { useAppDispatch, useAppSelector } from '../../store/store_hooks'
import { fight_selected, get_fight_selected } from '../../store/user_reports'
import Fight from '../../types/fight'
import { toMMSS } from '../../utils'

// @ts-ignore
import styles from "./FightWidget.scss"


function get_pull_color(percent: number) {
    if ( percent <=  3 ) { return "astounding" }
    if ( percent <= 10 ) { return "legendary" }
    if ( percent <= 25 ) { return "epic" }
    if ( percent <= 50 ) { return "rare" }
    if ( percent <= 75 ) { return "uncommon" }
    return "common"
}


interface FightWidgetProps {
    fight: Fight
    selected? : boolean
    onClick?: Function
}


export default function FightWidget({fight} : FightWidgetProps) {

    ////////////////////////////////
    const dispatch = useAppDispatch()
    const selected = useAppSelector(state => get_fight_selected(state, fight.fight_id))


    ////////////////////////////////
    function onClick() {
        dispatch(fight_selected({
            fight_id: fight.fight_id,
            selected: !selected,
        }))
    }

    ////////////////////////////////
    const pull_color = get_pull_color(fight.percent)

    ////////////////////////////////
    // Render
    return (
        <div
            className={`${styles.container} ${selected? "selected": ""} ${fight.kill ? "wow-kill": "wow-wipe"} p-1 border rounded`}
            onClick={onClick}
        >
            <span className={styles.label_pull}>#{fight.fight_id}</span>
            <span className={styles.label_duration}>({toMMSS(fight.duration/1000) })</span>

            {!fight.kill &&
                <div className={styles.pbar_outer}>
                    <div className={`${styles.pbar_inner} wow-${pull_color}`} style={{width: `${100-fight.percent}%`}} />
                    {/* <div className={styles.pbar_label}>{fight.percent}%</div> */}
                </div>
            }

        </div>
    )
}
