
import React from 'react'
import { useSelector } from 'react-redux'

import DisplaySettings from '../../components/SettingsBar/DisplaySettings.jsx'
import FilterSettings from '../../components/SettingsBar/FilterSettings/FilterSettings.jsx'
import SettingsBar from '../../components/SettingsBar/SettingsBar.jsx'
import SpecGroup from '../../components/SettingsBar/SpellSettings/SpecGroup.jsx'
import { BossSpellsGroup } from '../../components/SettingsBar/SpellSettings/SpellSettings.jsx'
import { get_boss } from '../../store/bosses.js'
import { get_spec } from '../../store/specs.js'


export default function SpecSettingsBar() {

    // Hooks
    const spec = useSelector(state => get_spec(state))
    const boss = useSelector(state => get_boss(state))

    // Render
    return (
        <SettingsBar>
            <DisplaySettings />
            <BossSpellsGroup />
            {spec && <SpecGroup spec={spec} />}

            {/* spacer to push filter settings to the right side */}
            <div className="ml-auto"></div>

            <FilterSettings />
        </SettingsBar>
    )
}
