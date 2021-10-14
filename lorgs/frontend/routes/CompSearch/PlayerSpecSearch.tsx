import CountFilterGroup from './SearchCountInput'
import FormGroup from './FormGroup'
import type Role from '../../types/role'
import { get_spec } from '../../store/specs'
import { useAppSelector } from '../../store/store_hooks'


function SpecSearchInput({spec_name} : {spec_name: string}) {

    const spec = useAppSelector(state => get_spec(state, spec_name))
    if (!spec) {
        // this can happen when the roles are already loaded, but the specs are not (yet)
        return null
    }

    return <CountFilterGroup
        name={`comp.spec.${spec.full_name_slug}`}
        icon_path={spec.icon_path}
        class_name={spec.class.name_slug}
    />
}

function create_spec_search_input_for_role(role: Role) {
    return (
        <div key={role.code} className="player-spec-search-row">
            {role.specs.map(spec_name => <SpecSearchInput key={spec_name} spec_name={spec_name} /> )}
        </div>
    )
}


export default function PlayerSpecSearch({className = ""}) {

    let roles_map = useAppSelector(state => state.roles)
    let roles = Object.values(roles_map).filter(role => role.id < 1000)

    return (
        <div className={className}>
            <FormGroup name="Specs:" className="player-spec-search">
                {roles.map(role => create_spec_search_input_for_role(role))}
            </FormGroup>
        </div>
    )
}
