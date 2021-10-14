import { get_spec } from "../../store/specs";
import { useAppSelector } from '../../store/store_hooks';
import type Role from '../../types/role';
import NavbarSpecsDropdown from './NavbarSpecsDropdown';

/*
    Button for a single role.
    Includes the specs dropdown that should show on hover
*/
export default function NavbarSpecRoleButton({ role } : { role: Role} ) {


    // check if the current spec is inside this role
    const current_spec = useAppSelector(state => get_spec(state));
    const has_active_child = current_spec && role.specs.find(spec => spec === current_spec.full_name_slug);

    const class_name = `wow-border-${role.code} ${has_active_child ? "active" : ""}`;

    // Render
    return (
        <div className="nav_dropdown">
            <img
                className={`role_button icon-spec icon-m border-black rounded ${class_name}`}
                src={role.icon_path}
                alt={role.name}
            />
            <NavbarSpecsDropdown key={role.code} specs={role.specs} />
        </div>
    );
}
