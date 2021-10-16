
import { NavLink, useRouteMatch } from 'react-router-dom';
import styles from  "./AdminNavbar.scss"

export default function AdminNavbar() {

    const {url } = useRouteMatch()

    return (
        <ul className={styles.nav}>
            <li className={styles.nav_item}>
                <NavLink to={`${url}/status`} className={styles.nav_item} activeClassName="active">Status</NavLink>
            </li>
            <li className={styles.nav_item}>
                <NavLink to={`${url}/spells`} className={styles.nav_item} activeClassName="active">Spells</NavLink>
            </li>
        </ul>
    )
}
