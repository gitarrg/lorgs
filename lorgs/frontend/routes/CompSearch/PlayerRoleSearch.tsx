
import React from 'react'
import { useSelector } from 'react-redux'
import FormGroup from './FormGroup'
import CountFilterGroup from './SearchCountInput'


/**
 * Group to search by role
 */
export default function PlayerRoleSearch() {

    let roles = useSelector(state => state.roles)
    roles = Object.values(roles).filter(role => role.id < 1000)

    return (
        <FormGroup name="Roles:" className="player-role-search">
            {roles.map(role =>
                <CountFilterGroup
                    key={role.code}
                    name={`role.${role.code}`}
                    icon_path={role.icon_path}
                    class_name={role.code}
                    tooltip={role.name || "hello?"}
                />
            )}
        </FormGroup>
    )
}
