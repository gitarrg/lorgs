

import React from 'react'
import { useSelector } from 'react-redux'

import ButtonGroup from '../shared/ButtonGroup'
import SpellButton from './SpellButton'
import { get_spec } from '../../../store/specs'
import { sort_spell_types } from '../../../store/ui'
import { get_used_spells } from '../../../store/spells'


// spell types that will be combined with the main spec
const COMBINED_TYPES = ["raid", "external", "defensive"]


function SpellTypeGroup({spec, spell_type}) {

    // fetch spells for combined types
    let spells = []

    let all_types = [spell_type]
    if (!spell_type.startsWith("other-")) {
        all_types = [...all_types, ...COMBINED_TYPES ]  // if its not an "other"-type, we merge in the combined types
    }

    all_types.forEach(type => {
        const type_spells = spec.spells_by_type[type] || []
        spells = [...spells, ...type_spells]
    })

    // check if there is a dedicated "spec" for the type (eg.: trinkets and potions)
    const type_spec = useSelector(state => get_spec(state, spell_type))
    spec = type_spec || spec
    const extra_class = "wow-text wow-" + spec.class.name_slug

    const was_used_spells = useSelector(state => get_used_spells(state))
    spells = spells.filter(spell_id =>  was_used_spells.includes(spell_id))
    if (spells.length == 0) { return null}

    return (
        <ButtonGroup name={spec.name || spec.full_name} side="left" extra_class={extra_class}>
            {spells.map(spell_id => <SpellButton key={spell_id} spec={spec} spell_id={spell_id} />)}
        </ButtonGroup>
    )
}


export default function SpecGroup({spec}) {

    if (!spec) { return }

    let spell_types = Object.keys(spec.spells_by_type || {})
    spell_types = sort_spell_types(spell_types)

    // skip combined groups
    spell_types = spell_types.filter(spell_type => !COMBINED_TYPES.includes(spell_type))

    // Render
    return spell_types.map(spell_type =>
        <SpellTypeGroup key={spell_type} spec={spec} spell_type={spell_type} />
    )
}
