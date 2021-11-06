/* SettingsBar for Reports */
import DisplaySettings from '../../components/SettingsBar/DisplaySettings'
import SettingsBar from '../../components/SettingsBar/SettingsBar'
import SpellSettings from '../../components/SettingsBar/SpellSettings/SpellSettings'


export default function ReportSettingsBar() {

    // Render
    return (
        <SettingsBar>
            <DisplaySettings />
            <SpellSettings />
            <div className="flex-grow-1"/>
        </SettingsBar>
    )
}
