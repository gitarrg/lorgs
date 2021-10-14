/* SettingsBar for Comp Reports

    Components:
    - default display settings
    - Healer Buttons (with dropdown for spells)
    - Raid CDs
    - <-- spacer ->
    - Filters
*/
import { Link } from 'react-router-dom';

import ButtonGroup from '../../components/SettingsBar/shared/ButtonGroup'
import DisplaySettings from '../../components/SettingsBar/DisplaySettings'
import RaidCDSpellButton from './RaidCDSpellButton'
import SettingsBar from '../../components/SettingsBar/SettingsBar'
import { BossSpellsGroup } from '../../components/SettingsBar/SpellSettings/SpellSettings'
import { RoleSpecsGroup } from '../../components/SettingsBar/RoleSpecDisplay'
import { get_role } from '../../store/roles'
import { get_spells_by_type } from '../../store/spells'
import { useAppSelector } from '../../store/store_hooks';


export default function CompSettingsBar() {

    // Get State Values
    const spells_by_type = useAppSelector(state => get_spells_by_type(state))
    const raid_cds = spells_by_type["raid"] ?? []
    const role_healer = useAppSelector(state => get_role(state, "heal"))

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

            <Link to="/comp_ranking/search" className="comp-search-button btn btn-primary shadow">
                Search
            </Link>

        </SettingsBar>
    )
}
