import { get_spec } from "../../store/specs";
import { useAppSelector } from '../../store/store_hooks';
import type Role from '../../types/role';
import NavbarSpecsDropdown from './NavbarSpecsDropdown';
import styles from "./Navbar.scss"
import WebpImg from "../WebpImg";

/*
    Button for a single role.
    Includes the specs dropdown that should show on hover
*/
export default function NavbarSpecRoleButton({ role } : { role: Role} ) {


    // check if the current spec is inside this role
    const current_spec = useAppSelector(state => get_spec(state));
    const has_active_child = current_spec && role.specs.find(spec => spec === current_spec.full_name_slug);

    // Render
    return (
        <div className={`${styles.dropdown_container}`}>

            {/* The Button itself */}
            <div className={`${styles.button} ${has_active_child ? "active" : ""}`} >
                <WebpImg
                    className={`icon-spec icon-m border-black rounded wow-border-${role.code}`}
                    src={role.icon_path}
                    alt={role.name}
                />
            </div>

            {/* The Dropdown */}
            <NavbarSpecsDropdown key={role.code} specs={role.specs} />
        </div>
    );
}
