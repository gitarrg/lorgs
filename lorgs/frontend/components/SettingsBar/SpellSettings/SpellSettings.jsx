
import React from 'react'

import AppContext from "./../../../AppContext/AppContext.jsx"
import ButtonGroup from './../shared/ButtonGroup.jsx'
import SpellButton from './SpellButton.jsx'



function _create_spell_buttons(spec = {}, spells=[]) {
    spells = spells || spec.spells || []
    return spec.spells.map(spell => <SpellButton key={`${spec.full_name_slug}/${spell.spell_id}`} spec={spec} spell={spell} />)
}


///////////////////////////////////////
// BOSS
//

function create_boss_group(boss = {}) {
    return (
        <ButtonGroup key="boss" name={boss.name} side="left" extra_class="wow-boss">
            {_create_spell_buttons(boss) }
        </ButtonGroup>
    )
}

///////////////////////////////////////
// SPECS
//

function create_spec_group(spec = {}, spells=[]) {

    const extra_class = "wow-" + spec.full_name_slug.split("-")[0]  // fixme
    return (
        <ButtonGroup key={spec.full_name_slug} name={spec.name} side="left" extra_class={extra_class}>
            {_create_spell_buttons(spec, spells) }
        </ButtonGroup>
    )

}


export default function SpellSettings() {

    const app_data = AppContext.getData()

    return (
        <>
            {create_boss_group(app_data.boss)}
            {app_data.specs.map(spec => create_spec_group(spec))}
        </>
    )
}
