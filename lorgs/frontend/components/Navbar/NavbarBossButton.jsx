
import { useSelector } from 'react-redux'
import { NavLink, useLocation } from 'react-router-dom';

import { MODES } from "../../data_store.js"

function get_link(mode, boss, spec) {
    // is this the time to rename "mode" ?
    if (mode == MODES.COMP_RANKING) { return `/${mode}/${boss.full_name_slug}` }
    if (mode == MODES.SPEC_RANKING) { return `/${mode}/${spec.full_name_slug}/${boss.full_name_slug}` }
    return "/"
}


export default function NavbarBossButton({boss}) {
    
    
    // todo: include zone in api?
    const icon_path = `/static/images/bosses/sanctum-of-domination/${boss.full_name_slug}.jpg`
    const mode = useSelector(state => state.mode)
    const spec = useSelector(state => state.spec)
    const link = get_link(mode, boss, spec)
    
    // preserve query string
    const { search } = useLocation();
    const full_link = `${link}${search}`

    return (
        <NavLink to={full_link} activeClassName="active">
            <img
                className="icon-spec icon-m wow-border-boss rounded"
                src={icon_path}
                alt={boss.name}
                data-tip={boss.full_name}
                alt={boss.full_name}
            />
        </NavLink>
    )
}

