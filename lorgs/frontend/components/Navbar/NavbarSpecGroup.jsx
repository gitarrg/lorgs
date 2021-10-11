
import { useSelector } from 'react-redux'
import { NavLink } from 'react-router-dom';

import { get_spec } from "../../store/specs.js"


function SpecButton({spec_slug}) {


    const mode = useSelector(state => state.ui.mode)
    const boss_slug = useSelector(state => state.ui.boss_slug)
    const spec = useSelector(state => get_spec(state, spec_slug))

    if (!spec) { return <p>nope: {spec_slug}</p>}

    const class_name = spec.class.name_slug
    const link = `/${mode}/${spec.full_name_slug}/${boss_slug}`

    return (

        <NavLink to={link} className={`wow-${class_name}`} activeClassName={`active`}>
            <img
                className={`mr-1 icon-spec icon-m rounded wow-border-${class_name}`}
                src={spec.icon_path}
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

    return (
        <div className="nav_dropdown__content specs_nav_dropdown bg-dark border rounded">
            <div className="p-2 d-grid gap-1">
                {specs.map(spec_slug => 
                    <SpecButton key={spec_slug} spec_slug={spec_slug} />
                )}
            </div>
        </div>
    )
}


function RoleButton({role}) {

    const class_name = `wow-border-${role.code}`

    return (
        <div className="nav_dropdown">
            <img
                className={`icon-spec icon-m border-black rounded ${class_name}`}
                src={role.icon_path}
                alt={role}
            />

            <SpecsDropdown key={role.code} specs={role.specs} />
        </div>
    )
}


export default function NavbarSpecGroup() {

    let roles = useSelector(state => state.roles)
    roles = Object.values(roles).filter(role => role.id < 1000)

    return (
        <>
            {roles.map(role =>
                <RoleButton key={role.code} role={role} />
            )}
        </>
    )
}
