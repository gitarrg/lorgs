import { useFormContext, useWatch } from 'react-hook-form';
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


export default function FightWidget({fight} : {fight: Fight}) {

    ////////////////////////////////
    const { setValue } = useFormContext();

    const attr_name = `fights[${fight.fight_id}]`

    ////////////////////////////////
    const pull_color = get_pull_color(fight.percent)
    const is_selected = useWatch({name: attr_name})

    ////////////////////////////////
    function toggle_selection() {
        setValue(attr_name, !is_selected)
    }

    ////////////////////////////////
    // Render
    return (
        <div
            className={`${styles.container} ${is_selected ? "selected": ""} ${fight.kill ? "wow-kill": "wow-wipe"} p-1 border rounded`}
            onClick={toggle_selection}
        >

            <span className={styles.label_pull}>Pull {fight.fight_id}</span>
            <span className={styles.label_duration}>({toMMSS(fight.duration/1000) })</span>

            {!fight.kill &&
                <div className={styles.pbar_outer}>
                    <div className={`${styles.pbar_inner} wow-${pull_color}`} style={{width: `${100-fight.percent}%`}} />
                    <div className={styles.pbar_label}>{fight.percent}%</div>
                </div>
            }

        </div>
    )
}
