import NavbarGroup from './NavbarGroup';
import NavbarSpecRoleButton from './NavbarSpecRoleButton';
import { get_player_roles } from "../../store/roles"
import { useAppSelector } from '../../store/store_hooks';


/*
    The entire group for all roles
*/
export default function NavbarSpecGroup() {

    const roles = useAppSelector(state => get_player_roles(state))

    return (
        <NavbarGroup>
            {roles.map(role =>
                <NavbarSpecRoleButton key={role.code} role={role} />
            )}
        </NavbarGroup>
    )
}
