import NavbarGroup from './NavbarGroup';
import NavbarSpecRoleButton from './NavbarSpecRoleButton';
import { get_roles } from "../../store/roles"
import { useAppSelector } from '../../store/store_hooks';


/*
    The entire group for all roles
*/
export default function NavbarSpecGroup() {

    let roles_map = useAppSelector(state => get_roles(state))
    let roles = Object.values(roles_map)
    roles = roles.filter(role => role.id < 1000)

    return (
        <NavbarGroup>
            {roles.map(role =>
                <NavbarSpecRoleButton key={role.code} role={role} />
            )}
        </NavbarGroup>
    )
}
