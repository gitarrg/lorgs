import Icon from '../../components/shared/Icon'
import PlayerWidget from './PlayerWidget'
import type Actor from '../../types/actor'
import type Role from '../../types/role'
import { get_player_roles } from '../../store/roles'
import { get_user_report_players } from  '../../store/user_reports'
import { group_by } from '../../utils'
import { useAppSelector } from '../../store/store_hooks'
import { SelectGroup } from './SelectGroup'


function RoleGroup({role, players} : {role: Role, players: Actor[]}) {
    if (!players) { return null }
    players = players.sort((a, b) => a.spec > b.spec ? -1 : 1)

    // Render
    const icon = <Icon spec={role} size="m"  />
    const items = players.map(player => <PlayerWidget key={player.source_id} player={player}/>)
    return <SelectGroup icon={icon} items={items} />
}


export default function PlayerSelectList() {

    const players = useAppSelector(state => get_user_report_players(state))
    const players_by_role = group_by(players, player => player.role)

    const roles = useAppSelector(state => get_player_roles(state))

    // Render
    return (
        <div className="d-flex flex-column gap-1">
            {Object.values(roles).map(role =>
                <RoleGroup key={role.code} role={role} players={players_by_role[role.code]} />
            )}
        </div>
    )
}
