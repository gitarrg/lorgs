/* SettingsBar for Comp Reports

    Components:
    - default display settings
    - Healer Buttons (with dropdown for spells)
    - Raid CDs
    - <-- spacer ->
    - Filters
*/
import React from 'react'
import { useSelector } from 'react-redux'

import ButtonGroup from '../../components/SettingsBar/shared/ButtonGroup.jsx'
import DisplaySettings from '../../components/SettingsBar/DisplaySettings.jsx'
import SettingsBar from '../../components/SettingsBar/SettingsBar.jsx'
import SpellButton from '../../components/SettingsBar/SpellSettings/SpellButton.jsx'
import { BossSpellsGroup } from '../../components/SettingsBar/SpellSettings/SpellSettings.jsx'
import { RoleSpecsGroup } from '../../components/SettingsBar/RoleSpecDisplay.jsx'


function get_spells_by_type(state, spell_type) {
    const all_spells = Object.values(state.spells)
    return all_spells.filter(spell => spell.spell_type == spell_type)
}



export default function CompSettingsBar() {


    // Get State Values
    const raid_cds = useSelector(state => get_spells_by_type(state, "raid"))
    const role_healer = useSelector(state => state.roles.find(role => role.code == "heal"))

    // Render
    return (
        <SettingsBar>

            <DisplaySettings />

            <BossSpellsGroup />

            {role_healer && <RoleSpecsGroup role={role_healer} />}

            <ButtonGroup name="Raid CDs" side="left">
                {raid_cds.map(spell => 
                    <SpellButton key={`raid_cd/${spell.spell_id}`} spell={spell} />
                )}
            </ButtonGroup>

            <div className="flex-grow-1"/>
        </SettingsBar>
    )
}
