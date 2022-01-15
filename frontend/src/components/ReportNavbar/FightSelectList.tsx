import FightWidget from "./FightWidget"
import Icon from "../shared/Icon"
import type Fight from "../../types/fight"
import { SelectGroup } from './SelectGrid/SelectGroup'
import { get_boss } from "../../store/bosses"
import { get_user_report_fights } from '../../store/user_reports'
import { group_by } from "../../utils"
import { useAppSelector } from '../../store/store_hooks'
import SelectGrid from "./SelectGrid/SelectGrid"


function BossGroup({boss_slug, fights} : {boss_slug: string, fights: Fight[]}) {

    const boss = useAppSelector(state => get_boss(state, boss_slug))
    if (!boss) { return null }

    // Render
    const icon = <Icon spec={boss} size="m" className="button grow-when-touched" />
    const items = fights.map(fight => <FightWidget key={fight.fight_id} fight={fight} />)
    return <SelectGroup icon={icon} items={items} />
}


export default function FightSelectList() {

    // Hooks
    const fights = useAppSelector(state => get_user_report_fights(state))
    if (fights.length == 0) { return null }

    // group fights by boss
    const fights_by_boss: {[key: string]: Fight[]} = group_by(fights, (fight: Fight) => fight.boss?.name)

    // render
    return (
        <SelectGrid title="Pulls:">
            {Object.keys(fights_by_boss).map(boss_slug =>
                <BossGroup key={boss_slug} boss_slug={boss_slug} fights={fights_by_boss[boss_slug]} />
            )}
        </SelectGrid>
    )
}
