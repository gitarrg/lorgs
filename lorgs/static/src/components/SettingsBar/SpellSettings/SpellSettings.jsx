
import React from 'react'

import AppDataContext from "./../../../AppDataContext.jsx"
import ButtonGroup from './../shared/ButtonGroup.jsx'
import SpellButton from './SpellButton.jsx'



function spell_group_key(spell) {
    if (!spell.group) { return "no group" }
    if (spell.group.role == "boss") { return "boss"}
    return spell.group.spec
}


function group_spells(spells) {
    // dict: group.full_name -> dict[group, spells]
    return spells.reduce((groups, spell) => {
        let key = spell_group_key(spell)
        groups[key] = (groups[key] || {...spell.group, spells: []});
        groups[key].spells.push(spell);
        return groups;
    }, {});
}


function create_spell_group(group) {

    if (!group) { return }

    let extra_class = "wow-" + group.spec.split("-")[0]
    if (group.role == "boss") { extra_class = "wow-boss"}

    return (
        <ButtonGroup key={group.name} name={group.name} extra_class={extra_class}>
            {group.spells.map(spell => (
                <SpellButton key={spell.spell_id} spell={spell} />
            ))}
        </ButtonGroup>
    )
}


export default function SpellSettings() {

    const ctx = React.useContext(AppDataContext)

    let spell_groups = group_spells(Object.values(ctx.spells))
    // this is to define the order
    const groups_names = ["boss", ctx.spec_slug, "other-potions", "other-trinkets"]

    return (
        <>
            {
                groups_names.map(group_name => (
                    create_spell_group(spell_groups[group_name])
                ))
            }
        </>
    )
}
