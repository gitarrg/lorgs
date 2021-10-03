import React from 'react'

import data_store, { MODES } from '../../data_store.js'
import DisplaySettings from './DisplaySettings.jsx'
import FilterSettings from "./FilterSettings/FilterSettings.jsx"
import RoleSpecDisplay from './RoleSpecDisplay/RoleSpecDisplay.jsx'
import SpellSettings from './SpellSettings/SpellSettings.jsx'

export default function SettingsBar() {

    const state = data_store.getState()

    const show_spells = state.mode != MODES.COMP_RANKING
    console.log(state, state.mode)

    return (
        <div className="settings_bar d-flex flex-row align-items-end flex-wrap mb-2">
            <DisplaySettings />

            <RoleSpecDisplay />

            { show_spells &&  <SpellSettings /> }

            <div className="flex-grow-1"/>

            <FilterSettings />
        </div>
    )
}
