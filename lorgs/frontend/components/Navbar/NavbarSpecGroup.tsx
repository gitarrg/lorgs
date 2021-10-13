
import { useSelector } from 'react-redux'

import NavbarGroup from './NavbarGroup';
import NavbarSpecRoleButton from './NavbarSpecRoleButton';
import { get_roles } from "../../store/roles"

/*
    The entire group for all roles
*/
export default function NavbarSpecGroup() {

    let roles_map = useSelector(state => get_roles(state))
    let roles = Object.values(roles_map)
    roles = roles.filter(role => role.id < 1000)

    return (
        <NavbarGroup className="navbar_specs" >
            {roles.map(role =>
                <NavbarSpecRoleButton key={role.code} role={role} />
            )}
        </NavbarGroup>
    )
}
