import React from 'react'
import { useSelector } from 'react-redux'
import CountFilterGroup from './SearchCountInput.jsx'


function create_spec_search_input(spec) {

    const icon_path = `/static/images/specs/${spec.full_name_slug}.jpg`
    return <CountFilterGroup
        key={spec.full_name_slug}
        name={`spec.${spec.full_name_slug}`}
        icon_path={icon_path}
        class_name={spec.class.name_slug}
    />
}

function create_spec_search_input_for_role(role) {
    return (
        <div key={role.code} className="player-spec-search-row">
            {role.specs.map(spec => create_spec_search_input(spec))}
        </div>
    )
}


export default function PlayerSpecSearch() {

    const roles = useSelector(state => state.roles.filter(role => role.id < 1000))
    return (
        <div className="ml-2">
            <h4 className="mb-0">Specs:</h4>
            <div className="player-spec-search bg-dark p-1 rounded border">
                {roles.map(role => create_spec_search_input_for_role(role))}
            </div>
        </div>
    )
}
