

import { useSelector, useDispatch } from 'react-redux'
import { get_spec } from '../../store/specs'
import { useAppDispatch, useAppSelector } from '../../store/store_hooks'
import { set_filter } from '../../store/ui'
import type Role from '../../types/role'

import ButtonGroup from './shared/ButtonGroup'
import FilterButton from './shared/FilterButton'


function create_role_button(role: Role) {

    const dispatch = useAppDispatch()

    function onClick({value} : {value: boolean}) {
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
function SpecDisplayButton({spec_slug} : {spec_slug: string}) {

    const dispatch = useAppDispatch()
    const spec = useAppSelector(state => get_spec(state, spec_slug))
    if (!spec) { return null } // not loaded yet

    function onClick({value} : {value: boolean}) {
        dispatch(set_filter({ group: "spec", name: spec_slug, value: value }))
    }

    return (
        <FilterButton
            onClick={onClick}
            name={spec.class.name_slug}
            full_name={spec.full_name}
            icon_name={`specs/${spec.full_name_slug}`}
        />
    )
}


export function RoleSpecsGroup({role} : {role: Role}) {
    return (
        <ButtonGroup name={role.name} side="left" extra_class={`wow-${role.code}`}>
            { role.specs.map(spec_slug => <SpecDisplayButton key={spec_slug} spec_slug={spec_slug} /> )}
        </ButtonGroup>
    )
}
