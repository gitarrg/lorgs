
import React from 'react'

import DisplaySettings from './DisplaySettings.jsx'
import FilterSettings from "./FilterSettings/FilterSettings.jsx"
import SpellSettings from './SpellSettings/SpellSettings.jsx'

export default function SettingsBar() {

    return (
        <div className="settings_bar d-flex flex-row align-items-end flex-wrap mb-2">
            <DisplaySettings />
            <SpellSettings />

            <div className="flex-grow-1"/>

            <FilterSettings />
        </div>
    )
}
