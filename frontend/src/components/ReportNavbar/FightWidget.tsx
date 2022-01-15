import SelectGridItem from "./SelectGrid/SelectGridItem"
import styles from "./FightWidget.scss"
import type Fight from '../../types/fight'
import { toMMSS, get_pull_color, timetamp_to_time } from '../../utils'


interface FightWidgetProps {
    fight: Fight
}


function format_percent(percent: number) {
    const digits = percent < 10 ? 1 : 0
    return percent.toFixed(digits)

}


export default function FightWidget({fight} : FightWidgetProps) {

    const field_name = `fight[${fight.fight_id}]`
    const pull_color = get_pull_color(fight.percent || 0)
    const className = `${styles.container} ${fight.kill ? "wow-kill": "wow-wipe"}`

    const label_percent = fight.kill ? "Kill! ⚑ " : `${format_percent(fight.percent || 0)}%`
    const label_time = timetamp_to_time(fight.time || 0)

    ////////////////////////////////
    // Render
    return (

        <SelectGridItem field_name={field_name} className={className}>
            <span className={styles.label_pull}>#{fight.fight_id}</span>
            <span className={styles.label_duration}>({toMMSS(fight.duration/1000) })</span>

            <span className={styles.label_percent}>{label_percent}</span>
            <span className={styles.label_time}>{label_time}</span>

            <>
            {!fight.kill &&
                <div className={styles.pbar_outer}>
                    <div className={`${styles.pbar_inner} wow-${pull_color}`} style={{width: `${100-(fight.percent || 0)}%`}} />
                </div>
            }
            </>
        </SelectGridItem>
    )
}
