

import React from 'react'
import { useSelector } from 'react-redux'

import AppContext from "./../../../AppContext/AppContext.jsx"
import ButtonGroup from './../shared/ButtonGroup.jsx'
import FilterButton from './../shared/FilterButton.jsx'
import data_store from '../../../data_store.js'



function create_role_button(role) {

    function onClick({value}) {
        data_store.dispatch({ type: "update_filter", field: role, value: value})
    }
    return <FilterButton onClick={onClick} key={role} name={role} icon_name={`roles/${role}`}/>
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


function RoleSpecsGroup({role}) {

    const show_role = useSelector(state => state.filters[role])
    if (show_role === false) { return null}
    
    const app_data = AppContext.getData()
    const specs = (app_data.specs || []).filter(spec => spec.role == role)

    return (
        <ButtonGroup name={role} side="left" extra_class={`wow-${role}`}>
            { specs.map(spec => create_display_spec_button(spec)) }
        </ButtonGroup>
    )
}



export default function RoleSpecDisplay() {

    return (
        <>
            <ButtonGroup name="Role" side="left">
                {create_role_button("tank")}
                {create_role_button("heal")}
                {create_role_button("mdps")}
                {create_role_button("rdps")}
            </ButtonGroup>

            <RoleSpecsGroup role="tank" />
            <RoleSpecsGroup role="heal" />
            <RoleSpecsGroup role="mdps" />
            <RoleSpecsGroup role="rdps" />
        </>
    )
}
