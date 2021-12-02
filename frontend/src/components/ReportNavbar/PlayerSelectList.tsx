import Icon from '../../components/shared/Icon'
import PlayerWidget from './PlayerWidget'
import SelectGrid from './SelectGrid/SelectGrid'
import type Actor from '../../types/actor'
import type Role from '../../types/role'
import { SelectGroup } from './SelectGrid/SelectGroup'
import { get_roles } from '../../store/roles'
import { get_user_report_players } from  '../../store/user_reports'
import { group_by } from '../../utils'
import { useAppSelector } from '../../store/store_hooks'


function RoleGroup({role, players} : {role: Role, players: Actor[]}) {
    if (!players) { return null }
    players = players.sort((a, b) => a.spec > b.spec ? -1 : 1)

    // Render
    const icon = <Icon spec={role} size="m" className="button grow-when-touched" />
    const items = players.map(player => <PlayerWidget key={player.source_id} player={player}/>)
    return <SelectGroup icon={icon} items={items} />
}


export default function PlayerSelectList() {

    const players = useAppSelector(get_user_report_players)
    const players_by_role = group_by(players, (player: Actor) => player.role || "mix")
    const roles = useAppSelector(get_roles)

    if (players.length == 0) { return null }

    // Render
    return (
        <SelectGrid title="Players:">
            {Object.values(roles).map(role =>
                <RoleGroup key={role.code} role={role} players={players_by_role[role.code]} />
            )}
        </SelectGrid>
    )
}
