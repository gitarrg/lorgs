
import { NavLink, useRouteMatch } from 'react-router-dom';
import "./AdminNavbar.scss"

export default function AdminNavbar() {

    const {url } = useRouteMatch()

    return (
        <ul className="nav">
            <li className="nav-item">
                <NavLink to={`${url}/status`} className="nav-link" activeClassName="active">Status</NavLink>
            </li>
            <li className="nav-item">
                <NavLink to={`${url}/spells`} className="nav-link" activeClassName="active">Spells</NavLink>
            </li>
        </ul>
    )
}
