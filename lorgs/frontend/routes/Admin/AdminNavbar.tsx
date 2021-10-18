
import { NavLink, useRouteMatch } from 'react-router-dom';
import styles from  "./AdminNavbar.scss"

export default function AdminNavbar() {

    const {url } = useRouteMatch()

    return (
        <nav className={styles.nav}>
            <NavLink to={`${url}/status`} className={styles.nav_link} activeClassName="active">Status</NavLink>
            <NavLink to={`${url}/spells`} className={styles.nav_link} activeClassName="active">Spells</NavLink>
        </nav>
    )
}
