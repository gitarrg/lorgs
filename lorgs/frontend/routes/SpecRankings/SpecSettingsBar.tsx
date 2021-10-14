
import React from 'react'

import DisplaySettings from '../../components/SettingsBar/DisplaySettings'
import FilterSettings from '../../components/SettingsBar/FilterSettings/FilterSettings'
import SettingsBar from '../../components/SettingsBar/SettingsBar'
import SpecGroup from '../../components/SettingsBar/SpellSettings/SpecGroup'
import { BossSpellsGroup } from '../../components/SettingsBar/SpellSettings/SpellSettings'
import { get_spec } from '../../store/specs'
import { useAppSelector } from '../../store/store_hooks'


export default function SpecSettingsBar() {

    // Hooks
    const spec = useAppSelector(state => get_spec(state))

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
