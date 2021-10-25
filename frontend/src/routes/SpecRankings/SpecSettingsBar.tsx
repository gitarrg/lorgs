import DisplaySettings from '../../components/SettingsBar/DisplaySettings'
import FilterSettings from '../../components/SettingsBar/FilterSettings/FilterSettings'
import SettingsBar from '../../components/SettingsBar/SettingsBar'
import SpecGroup from '../../components/SettingsBar/SpellSettings/SpecGroup'
import { BossSpellsGroup } from '../../components/SettingsBar/SpellSettings/SpellSettings'


export default function SpecSettingsBar() {



    // Render
    return (
        <SettingsBar>
            <DisplaySettings />
            <BossSpellsGroup />
            <SpecGroup />

            {/* spacer to push filter settings to the right side */}
            <div className="ml-auto"></div>

            <FilterSettings />
        </SettingsBar>
    )
}
