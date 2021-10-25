import FightWidget from "./FightWidget"
import Icon from "../shared/Icon"
import type Fight from "../../types/fight"
import { SelectGroup } from './SelectGroup'
import { get_boss } from "../../store/bosses"
import { get_user_report_fights } from '../../store/user_reports'
import { group_by } from "../../utils"
import { useAppSelector } from '../../store/store_hooks'


function BossGroup({boss_slug, fights} : {boss_slug: string, fights: Fight[]}) {

    const boss = useAppSelector(state => get_boss(state, boss_slug))
    if (!boss) { return null }

    // Render
    const icon = <Icon spec={boss} size="m"  />
    const items = fights.map(fight => <FightWidget key={fight.fight_id} fight={fight} />)
    return <SelectGroup icon={icon} items={items} />
}


export default function FightSelectList() {

    // Hooks
    const fights = useAppSelector(state => get_user_report_fights(state))
    if (!fights) { return null }

    // group fights by boss
    const fights_by_boss: {[key: string]: Fight[]} = group_by(fights, fight => fight.boss_slug)

    // render
    return (
        <div className="d-flex flex-column gap-3">
            {Object.keys(fights_by_boss).map(boss_slug =>
                <BossGroup key={boss_slug} boss_slug={boss_slug} fights={fights_by_boss[boss_slug]} />
            )}
        </div>
    )
}
