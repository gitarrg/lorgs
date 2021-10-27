import ButtonGroup from '../shared/ButtonGroup'
import SpellButton from './SpellButton'
import type Spec from '../../../types/spec'
import { get_spec } from '../../../store/specs'
import { get_used_spells } from '../../../store/spells'
import { sort_spell_types } from '../../../store/ui'
import { useAppSelector } from '../../../store/store_hooks'



function SpellTypeGroup({spell_type}: {spell_type: string}  ) {


    const spec = useAppSelector(state => get_spec(state, spell_type))
    const all_spells = useAppSelector(get_spells_by_type)
    const used_spells = useAppSelector(get_used_spells)
    const type_spells = all_spells[spell_type] || []
    const spells = type_spells.filter(spell_id =>  used_spells.includes(spell_id))

    if (!spec) { return null }
    if (spells.length === 0) { return null }

    console.log("spec", spec)

    const extra_class = "wow-" + spec.class.name_slug

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


export default function SpecGroup({spec_slug=""}) {

    // Hooks


    // let spell_types = Object.keys(spec.spells_by_type || {})
    // spell_types = sort_spell_types(spell_types)

    const spell_types = [spec_slug]

    // Render
    return (
        <>
            {spell_types.map(spell_type =>
                <SpellTypeGroup key={spell_type} spell_type={spell_type} />
            )}
        </>
    )
}
