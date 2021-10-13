import { useSelector } from 'react-redux';
import { get_spec } from "../../store/specs";
import NavbarSpecsDropdown from './NavbarSpecsDropdown';

/*
    Button for a single role.
    Includes the specs dropdown that should show on hover
*/
export default function NavbarSpecRoleButton({ role }) {


    // check if the current spec is inside this role
    const current_spec = useSelector(state => get_spec(state));
    const has_active_child = current_spec && role.specs.find(spec => spec === current_spec.full_name_slug);

    const class_name = `wow-border-${role.code} ${has_active_child ? "active" : ""}`;

    // Render
    return (
        <div className="nav_dropdown">
            <img
                className={`role_button icon-spec icon-m border-black rounded ${class_name}`}
                src={role.icon_path}
                alt={role} />

            <NavbarSpecsDropdown key={role.code} specs={role.specs} />
        </div>
    );
}
