
import { useSelector } from 'react-redux'
import { NavLink } from 'react-router-dom';

import data_store from "../../data_store.js"


function SpecButton({spec}) {

    const icon_path = `/static/images/specs/${spec.full_name_slug}.jpg`
    const class_name = spec.class.name_slug

    const state = data_store.getState()
    const link = `/${state.mode}/${spec.full_name_slug}/${state.boss.full_name_slug}`

    return (
        <NavLink to={link} activeClassName="active">
            <img
                className={`mr-1 icon-spec icon-m rounded wow-border-${class_name}`}
                src={icon_path}
                alt={spec.full_name}
                title={spec.full_name}
            />

            <span className={`wow-${class_name}`}>
                {spec.full_name}
            </span>
        </NavLink>
    )
}


function SpecsDropdown({specs}) {

    // <div class="ranking-nav-role-specs bg-dark border rounded"></div>

    return (
        <div className="nav_dropdown__content specs_nav_dropdown bg-dark border rounded">
            <div className="p-2 d-grid gap-1">
                {specs.map(spec => 
                    <SpecButton key={spec.full_name_slug} spec={spec} />
                )}
            </div>
        </div>
    )
}


function RoleButton({role}) {

    const icon_path = `/static/images/roles/${role.code}.jpg`
    const class_name = `wow-border-${role.code}`

    return (
        <div className="nav_dropdown">
            <img
                className={`icon-spec icon-m border-black rounded ${class_name}`}
                src={icon_path}
                alt={role}
            />

            <SpecsDropdown key={role.code} specs={role.specs} />
        </div>
    )
}


export default function NavbarSpecGroup() {

    let roles = useSelector(state => state.roles)
    roles = roles.filter(role => role.id <= 1000) // filter out data roles

    return (
        <>
            {roles.map(role =>
                <RoleButton key={role.code} role={role} />
            )}
        </>
    )
}
