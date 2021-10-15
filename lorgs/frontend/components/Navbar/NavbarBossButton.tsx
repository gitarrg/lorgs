import { NavLink, useLocation } from 'react-router-dom';

import type Boss from "../../types/boss"
import type Spec from "../../types/spec"
import { MODES } from '../../store/ui';
import { get_spec } from "../../store/specs"
import { useAppSelector } from '../../store/store_hooks';
import styles from "./Navbar.scss"


function get_link(mode : string, boss: Boss, spec?: Spec) {
    // is this the time to rename "mode" ?
    if (mode == MODES.COMP_RANKING) { return `/${mode}/${boss.full_name_slug}` }
    if (mode == MODES.SPEC_RANKING) { return `/${mode}/${spec?.full_name_slug}/${boss.full_name_slug}` }
    return "/"
}


export default function NavbarBossButton({boss} : {boss: Boss}) {

    // todo: include zone in api?
    const mode = useAppSelector(state => state.ui.mode)
    const spec = useAppSelector(state => get_spec(state))
    const link = get_link(mode, boss, spec)

    // preserve query string
    const { search } = useLocation();
    const full_link = `${link}${search}`

    return (
        <NavLink to={full_link} className={styles.button} activeClassName="active" data-tooltip={boss.full_name} data-tooltip-dir="down">
            <img
                className="icon-spec icon-m wow-boss wow-border rounded"
                src={boss.icon_path}
                alt={boss.full_name}
            />
        </NavLink>
    )
}

