import ButtonGroup from '../shared/ButtonGroup'
import SpellButton from './SpellButton'
import type Spec from '../../../types/spec'
import { get_spec } from '../../../store/specs'
import { get_used_spells } from '../../../store/spells'
import { sort_spell_types } from '../../../store/ui'
import { useAppSelector } from '../../../store/store_hooks'



function SpellTypeGroup({spec, spell_type}: {spec: Spec, spell_type: string}  ) {

    // fetch spells for combined types
    // let spells: number[] = []
    let spells = spec.spells_by_type[spell_type] || []

    // check if there is a dedicated "spec" for the type (eg.: trinkets and potions)
    const type_spec = useAppSelector(state => get_spec(state, spell_type))
    spec = type_spec || spec
    const extra_class = "wow-" + spec.class.name_slug

    const used_spells = useAppSelector(state => get_used_spells(state))
    spells = spells.filter(spell_id =>  used_spells.includes(spell_id))
    if (spells.length == 0) { return null}

    // Build a nice Group Name: either the Spec- or Class Name
    let group_name = spec.name || spec.full_name
    if (spell_type == spec.class.name_slug) {
        group_name = spec.class.name
    }

    return (
        <ButtonGroup name={group_name} side="left" extra_class={extra_class}>
            {spells.map(spell_id => <SpellButton key={spell_id} spec={spec} spell_id={spell_id} />)}
        </ButtonGroup>
    )
}


export default function SpecGroup({spec} : {spec: Spec }) {

    if (!spec) { return null }

    let spell_types = Object.keys(spec.spells_by_type || {})
    spell_types = sort_spell_types(spell_types)

    // Render
    return (
        <>
            {spell_types.map(spell_type =>
                <SpellTypeGroup key={spell_type} spec={spec} spell_type={spell_type} />
            )}
        </>
    )
}
