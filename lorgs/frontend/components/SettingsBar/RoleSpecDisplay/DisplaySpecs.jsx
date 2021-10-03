

import React from 'react'
import ButtonGroup from './shared/ButtonGroup.jsx'
import AppContext from "./../../AppContext/AppContext.jsx"
import FilterButton from './shared/FilterButton.jsx'


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

function create_role_group(role, app_data) {

    const specs = app_data.specs.filter(spec => spec.role == role)

    return (
        <ButtonGroup name={role} side="left" extra_class={`wow-${role}`}>

            {
                specs.map(spec => create_display_spec_button(spec))
            }

        </ButtonGroup>
    )

}


export default function DisplaySpecGroup() {
    
    const shared_classes = "button icon-s rounded border-white"
    
    const app_data = AppContext.getData()


    return (
        <>
            {create_role_group("tank", app_data)}
            {create_role_group("heal", app_data)}
            {create_role_group("mdps", app_data)}
            {create_role_group("rdps", app_data)}
        </>
    )
}
