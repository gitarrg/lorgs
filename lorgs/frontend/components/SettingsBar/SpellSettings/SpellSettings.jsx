
import React from 'react'
import { useSelector } from 'react-redux'

import ButtonGroup from './../shared/ButtonGroup.jsx'
import SpellButton from './SpellButton.jsx'



function _create_spell_buttons(spec = {}) {
    return spec.spells.map(spell => <SpellButton key={`${spec.full_name_slug}/${spell.spell_id}`} spec={spec} spell={spell} />)
}


///////////////////////////////////////
// BOSS
//

export function BossSpellsGroup() {

    const boss = useSelector(state => state.boss)

    return (
        <ButtonGroup key="boss" name={boss.name} side="left" extra_class="wow-boss">
            {_create_spell_buttons(boss) }
        </ButtonGroup>
    )
}

///////////////////////////////////////
// SPECS
//

function create_spec_group(spec = {}) {

    const extra_class = "wow-" + spec.full_name_slug.split("-")[0]  // fixme

    return (
        <ButtonGroup key={spec.full_name_slug} name={spec.name} side="left" extra_class={extra_class}>
            {_create_spell_buttons(spec) }
        </ButtonGroup>
    )
}


export default function SpellSettings() {

    const specs = useSelector(state => state.specs)

    return (
        <>
            <BossSpellsGroup />
            {specs.map(spec => create_spec_group(spec))}
        </>
    )
}
