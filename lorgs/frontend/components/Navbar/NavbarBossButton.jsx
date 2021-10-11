
import { useSelector } from 'react-redux'
import { NavLink, useLocation } from 'react-router-dom';

import { MODES } from '../../store/ui.js';
import { get_spec } from "../../store/specs.js"


function get_link(mode, boss = {}, spec = {}) {
    // is this the time to rename "mode" ?
    if (mode == MODES.COMP_RANKING) { return `/${mode}/${boss.full_name_slug}` }
    if (mode == MODES.SPEC_RANKING) { return `/${mode}/${spec.full_name_slug}/${boss.full_name_slug}` }
    return "/"
}


export default function NavbarBossButton({boss}) {

    // todo: include zone in api?
    const mode = useSelector(state => state.ui.mode)
    const spec = useSelector(state => get_spec(state))
    const link = get_link(mode, boss, spec)

    // preserve query string
    const { search } = useLocation();
    const full_link = `${link}${search}`

    return (
        <NavLink to={full_link} activeClassName="active" data-tooltip={boss.full_name} data-tooltip-dir="down">
            <img
                className="icon-spec icon-m wow-boss wow-border rounded"
                src={boss.icon_path}
                alt={boss.full_name}
            />
        </NavLink>
    )
}

