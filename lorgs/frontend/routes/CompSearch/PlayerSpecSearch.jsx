import React from 'react'
import { useSelector } from 'react-redux'
import { get_spec } from '../../store/specs.js'
import CountFilterGroup from './SearchCountInput.jsx'


function SpecSearchInput({spec_name}) {

    const spec = useSelector(state => get_spec(state, spec_name))
    if (!spec) {
        // this can happen when the roles are already loaded, but the specs are not (yet)
        return null
    }

    return <CountFilterGroup
        name={`spec.${spec.full_name_slug}`}
        icon_path={spec.icon_path}
        class_name={spec.class.name_slug}
    />
}

function create_spec_search_input_for_role(role) {
    return (
        <div key={role.code} className="player-spec-search-row">
            {role.specs.map(spec_name => <SpecSearchInput key={spec_name} spec_name={spec_name} /> )}
        </div>
    )
}


export default function PlayerSpecSearch() {

    let roles = useSelector(state => state.roles)
    roles = Object.values(roles).filter(role => role.id < 1000)

    return (
        <div className="ml-2">
            <h4 className="mb-0">Specs:</h4>
            <div className="player-spec-search bg-dark p-1 rounded border">
                {roles.map(role => create_spec_search_input_for_role(role))}
            </div>
        </div>
    )
}
