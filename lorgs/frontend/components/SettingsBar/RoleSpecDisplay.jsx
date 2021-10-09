

import React from 'react'
import { useSelector, useDispatch } from 'react-redux'

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


function create_display_spec_button(spec) {
    return (
        <FilterButton
            key={spec.full_name_slug}
            name={spec.class.name_slug}
            full_name={spec.full_name_slug}
            icon_name={`specs/${spec.full_name_slug}`}
        />
    )
}


export function RoleSpecsGroup({role}) {

    const show_role = useSelector(state => state.filters[role.code])
    if (show_role === false) { return null}

    return (
        <ButtonGroup name={role.name} side="left" extra_class={`wow-${role.code}`}>
            { role.specs.map(spec => create_display_spec_button(spec)) }
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
