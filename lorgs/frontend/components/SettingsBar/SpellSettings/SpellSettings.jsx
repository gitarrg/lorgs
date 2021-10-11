
import React from 'react'
import { useSelector } from 'react-redux'

import ButtonGroup from './../shared/ButtonGroup.jsx'
import SpellButton from './SpellButton.jsx'
import { get_boss } from '../../../store/bosses.js'

// TODO: is this even used anymore?

function _create_spell_buttons(spec) {
    if ( !spec.spells ) { return }
    return spec.spells.map(spell_id => <SpellButton key={`${spec.full_name_slug}/${spell_id}`} spec={spec} spell_id={spell_id} />)
}


///////////////////////////////////////
// BOSS
//

export function BossSpellsGroup() {

    const boss = useSelector(state => get_boss(state))

    return (
        <ButtonGroup key="boss" name={boss.name} side="left" extra_class="wow-text wow-boss">
            {_create_spell_buttons(boss) }
        </ButtonGroup>
    )
}

///////////////////////////////////////
// SPECS
//

function create_spec_group(spec = {}) {

    const extra_class = "wow-text wow-" + spec.class.name_slug

    const spells = spec.spells || []
    if (!spells) { return }

    return (
        <ButtonGroup key={spec.full_name_slug} name={spec.name} side="left" extra_class={extra_class}>
            {_create_spell_buttons(spec) }
        </ButtonGroup>
    )
}


export default function SpellSettings() {

    const specs = useSelector(state =>  state.specs)
    console.log("SpellSettings", specs)

    return (
        <>
            <BossSpellsGroup />
            {Object.values(specs).map(spec => create_spec_group(spec))}
        </>
    )
}
