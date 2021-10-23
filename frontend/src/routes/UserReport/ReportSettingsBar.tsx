/* SettingsBar for Reports */
import DisplaySettings from '../../components/SettingsBar/DisplaySettings'
import SettingsBar from '../../components/SettingsBar/SettingsBar'
import { BossSpellsGroup } from '../../components/SettingsBar/SpellSettings/SpellSettings'

export default function ReportSettingsBar() {

    // Render
    return (
        <SettingsBar>
            <DisplaySettings />
            <BossSpellsGroup />
            <div className="flex-grow-1"/>
        </SettingsBar>
    )
}
