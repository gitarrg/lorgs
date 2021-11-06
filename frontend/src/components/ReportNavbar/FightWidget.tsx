import SelectGridItem from "./SelectGrid/SelectGridItem"
import styles from "./FightWidget.scss"
import type Fight from '../../types/fight'
import { toMMSS } from '../../utils'


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
}


export default function FightWidget({fight} : FightWidgetProps) {

    const field_name = `fight[${fight.fight_id}]`
    const pull_color = get_pull_color(fight.percent || 0)
    const className = `${styles.container} ${fight.kill ? "wow-kill": "wow-wipe"}`

    ////////////////////////////////
    // Render
    return (

        <SelectGridItem field_name={field_name} className={className}>
            <span className={styles.label_pull}>#{fight.fight_id}</span>
            <span className={styles.label_duration}>({toMMSS(fight.duration/1000) })</span>

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
