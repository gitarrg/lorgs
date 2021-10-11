
import { useSelector } from 'react-redux'

import NavbarGroup from './NavbarGroup.jsx';
import NavbarSpecRoleButton from './NavbarSpecRoleButton.jsx';


/*
    The entire group for all roles
*/
export default function NavbarSpecGroup() {

    let roles = useSelector(state => state.roles)
    roles = Object.values(roles).filter(role => role.id < 1000)

    return (
        <NavbarGroup className="navbar_specs" >
            {roles.map(role =>
                <NavbarSpecRoleButton key={role.code} role={role} />
            )}
        </NavbarGroup>
    )
}
