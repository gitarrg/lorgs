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
import { BossSpellsGroup } from '../../components/SettingsBar/SpellSettings/SpellSettings.jsx'
import { RoleSpecsGroup } from '../../components/SettingsBar/RoleSpecDisplay.jsx'
import { get_role } from '../../store/roles.js'
import { get_spells_by_type } from '../../store/spells.js'
import RaidCDSpellButton from './RaidCDSpellButton.jsx'




export default function CompSettingsBar() {


    // Get State Values
    const spells_by_type = useSelector(state => get_spells_by_type(state))
    const raid_cds = spells_by_type["raid"] || []
    const role_healer = useSelector(state => get_role(state, "heal"))

    // Render
    return (
        <SettingsBar>

            <DisplaySettings />

            <BossSpellsGroup />

            {role_healer && <RoleSpecsGroup role={role_healer} />}

            <ButtonGroup name="Raid CDs" side="left">
                {raid_cds.map(spell =>
                    <RaidCDSpellButton key={`raid_cd/${spell.spell_id}`} spell_id={spell.spell_id} />
                 )}
            </ButtonGroup>

            <div className="flex-grow-1"/>
        </SettingsBar>
    )
}
