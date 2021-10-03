

import React from 'react'
import ButtonGroup from './shared/ButtonGroup.jsx'
import AppContext from "./../../AppContext/AppContext.jsx"
import FilterButton from './shared/FilterButton.jsx'


function create_role_button(role) {

    function toggle_role() {

        console.log("show/hide", role)

    }

    return <FilterButton onClick={toggle_role} key={role} name={role} icon_name={`roles/${role}`}/>
}


export default function RoleDisplayGroup() {
    
    return (
        <>
            <ButtonGroup name="Role" side="left">
                {create_role_button("tank")}
                {create_role_button("heal")}
                {create_role_button("mdps")}
                {create_role_button("rdps")}
            </ButtonGroup>
        </>
    )
}
