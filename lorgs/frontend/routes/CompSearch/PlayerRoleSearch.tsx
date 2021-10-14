
import { useAppSelector } from '../../store/store_hooks'
import FormGroup from './FormGroup'
import CountFilterGroup from './SearchCountInput'


/**
 * Group to search by role
 */
export default function PlayerRoleSearch() {

    let roles_map = useAppSelector(state => state.roles)
    let roles = Object.values(roles_map).filter(role => role.id < 1000)

    return (
        <FormGroup name="Roles:" className="player-role-search">
            {roles.map(role =>
                <CountFilterGroup
                    key={role.code}
                    name={`role.${role.code}`}
                    icon_path={role.icon_path}
                    class_name={role.code}
                />
            )}
        </FormGroup>
    )
}
