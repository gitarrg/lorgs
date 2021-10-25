/* SettingsBar for Reports */
import DisplaySettings from '../../components/SettingsBar/DisplaySettings'
import SettingsBar from '../../components/SettingsBar/SettingsBar'
import SpecGroup from '../../components/SettingsBar/SpellSettings/SpecGroup'
import { BossSpellsGroup } from '../../components/SettingsBar/SpellSettings/SpellSettings'
import { get_occuring_bosses, get_occuring_specs } from '../../store/fights'
import { useAppSelector } from '../../store/store_hooks'



function BossGroups() {

    const bosses = useAppSelector(get_occuring_bosses)
    return <>
        {bosses.map(boss_slug =>
        <BossSpellsGroup key={boss_slug} boss_slug={boss_slug}/>
    )}
    </>
}

function SpecGroups() {

    const specs = useAppSelector(get_occuring_specs)

    return <>
        {specs.map(spec_slug =>
            <SpecGroup key={spec_slug} spec_slug={spec_slug} />
        )}
    </>
}


export default function ReportSettingsBar() {

    // Render
    return (
        <SettingsBar>
            <DisplaySettings />
            <BossGroups />
            <SpecGroups />
            <div className="flex-grow-1"/>
        </SettingsBar>
    )
}
