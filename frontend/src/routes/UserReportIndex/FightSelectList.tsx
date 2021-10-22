import FightWidget from "./FightWidget"
import { get_user_report_fights } from '../../store/user_reports'
import { useAppSelector } from '../../store/store_hooks'
import type Fight from "../../types/fight"
import { group_by } from "../../utils"
import Icon from "../../components/shared/Icon"

// @ts-ignore
import styles from "./FightSelectList.scss"
import { get_boss } from "../../store/bosses"


function BossGroup({boss_slug, fights} : {boss_slug: string, fights: Fight[]}) {

    const boss = useAppSelector(state => get_boss(state, boss_slug))
    if (!boss) { return }

    // Render
    return (
        <div className={styles.boss_group}>
            <div className={styles.boss_frame} data-tooltip={boss.full_name}>
                <Icon spec={boss} size="l"  />
            </div>

            <div className={styles.fights_group}>
                {fights.map(fight =>
                    <FightWidget key={fight.fight_id} fight={fight} />
                )}
            </div>
        </div>
    )
}


export default function FightSelectList() {

    // Hooks
    const fights = useAppSelector(state => get_user_report_fights(state))
    if (!fights) { return null }

    // group fights by boss
    const fights_by_boss: {[key: string]: Fight[]} = group_by(fights, fight => fight.boss_slug)

    // render
    return (
        <div className={`${styles.container} rounded p-2`}>
            {Object.keys(fights_by_boss).map(boss_slug =>
                <BossGroup key={boss_slug} boss_slug={boss_slug} fights={fights_by_boss[boss_slug]} />
            )}
        </div>
    )
}
