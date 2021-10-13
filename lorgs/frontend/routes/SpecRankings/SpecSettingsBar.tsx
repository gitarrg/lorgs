
import React from 'react'
import { useSelector } from 'react-redux'

import DisplaySettings from '../../components/SettingsBar/DisplaySettings'
import FilterSettings from '../../components/SettingsBar/FilterSettings/FilterSettings'
import SettingsBar from '../../components/SettingsBar/SettingsBar'
import SpecGroup from '../../components/SettingsBar/SpellSettings/SpecGroup'
import { BossSpellsGroup } from '../../components/SettingsBar/SpellSettings/SpellSettings'
import { get_boss } from '../../store/bosses'
import { get_spec } from '../../store/specs'


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
