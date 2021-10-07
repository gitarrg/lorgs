
import React from 'react'
import { useSelector } from 'react-redux'
import FormGroup from './FormGroup.jsx'
import CountFilterGroup from './SearchCountInput.jsx'


function RoleSearchInput({role}) {

    const icon_path = `/static/images/roles/${role.code}.jpg`

    return (
        <>
        <div className="search_spec_row">
            <CountFilterGroup
                name={`role.${role.code}`}
                icon_path={icon_path}
                class_name={role.code}
            />
        </div>
        </>
    )
}


/* Group to search by role */
export default function PlayerRoleSearch() {

    const roles = useSelector(state => state.roles.filter(role => role.id < 1000))

    return (
        <FormGroup name="Roles:" className="player-role-search">
            {roles.map(role => <RoleSearchInput key={role.code} role={role} /> )}
        </FormGroup>
    )
}
