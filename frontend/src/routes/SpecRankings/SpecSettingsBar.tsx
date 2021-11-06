import DisplaySettings from '../../components/SettingsBar/DisplaySettings'
import FilterSettings from '../../components/SettingsBar/FilterSettings/FilterSettings'
import SettingsBar from '../../components/SettingsBar/SettingsBar'
import SpellSettings from '../../components/SettingsBar/SpellSettings/SpellSettings'


export default function SpecSettingsBar() {

    // Render
    return (
        <SettingsBar>
            <DisplaySettings />
            <SpellSettings />
            {/* spacer to push filter settings to the right side */}
            <div className="ml-auto"></div>

            <FilterSettings />
        </SettingsBar>
    )
}
