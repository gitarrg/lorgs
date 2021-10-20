import NavBarSpecButton from './NavBarSpecButton';
import styles from "./Navbar.scss"

export default function NavbarSpecsDropdown({ specs } : { specs: string[] }) {

    // Inputs
    const specs_sorted = [...specs].sort();

    // Render
    return (
        <div className={`${styles.dropdown_container__dropdown} bg-dark border rounded p-2`}>
            <div className={styles.dropdown_content}>
                {specs_sorted.map(spec_slug => <NavBarSpecButton key={spec_slug} spec_slug={spec_slug} />)}
            </div>
        </div>
    );
}
