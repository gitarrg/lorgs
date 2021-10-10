

import React from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { get_spec } from '../../store/specs.js'
import { set_filter } from '../../store/ui.js'

import ButtonGroup from './shared/ButtonGroup.jsx'
import FilterButton from './shared/FilterButton.jsx'


function create_role_button(role) {

    const dispatch = useDispatch()

    function onClick({value}) {
        dispatch({ type: "update_filter", field: role.code, value: value})
    }
    return <FilterButton
        onClick={onClick}
        key={role.code}
        name={role.code}
        full_name={role.name}
        icon_name={`roles/${role.code}`}
    />
}


/*
    Button to show/display a single spec
*/
function SpecDisplayButton({spec_slug}) {

    const dispatch = useDispatch()
    const spec = useSelector(state => get_spec(state, spec_slug))
    if (!spec) { return null } // not loaded yet

    function onClick({value}) {
        dispatch(set_filter({ group: "spec", name: spec_slug, value: value }))
    }

    return (
        <FilterButton
            onClick={onClick}
            name={spec.class.name_slug}
            full_name={spec.full_name_slug}
            icon_name={`specs/${spec.full_name_slug}`}
        />
    )
}


export function RoleSpecsGroup({role}) {
    return (
        <ButtonGroup name={role.name} side="left" extra_class={`wow-${role.code}`}>
            { role.specs.map(spec_slug => <SpecDisplayButton key={spec_slug} spec_slug={spec_slug} /> )}
        </ButtonGroup>
    )
}



export default function RoleSpecDisplay({roles}) {

    if (!roles) {
        roles = roles || useSelector(state => state.roles)
        roles = roles.filter(role => role.id <= 1000) // filter out data roles
    }

    return (
        <>
            <ButtonGroup name="Role" side="left">
                {roles.map(role => create_role_button(role))}
            </ButtonGroup>

            {roles.map(role => <RoleSpecsGroup key={role.code} role={role} /> )}
        </>
    )
}
