import React from 'react'

import DisplaySettings from './DisplaySettings.jsx'
import FilterSettings from "./FilterSettings/FilterSettings.jsx"
import RoleSpecDisplay from './RoleSpecDisplay/RoleSpecDisplay.jsx'
import SpellSettings from './SpellSettings/SpellSettings.jsx'
import data_store, { MODES } from '../../data_store.js'

export default function SettingsBar() {

    const state = data_store.getState()
    const mode_comps = state.mode == MODES.COMP_RANKING
    const mode_specs = state.mode == MODES.SPEC_RANKING

    return (
        <div className="settings_bar d-flex flex-row align-items-end flex-wrap mb-2">
            <DisplaySettings />
                { mode_comps && <RoleSpecDisplay /> }
                { mode_specs &&  <SpellSettings /> }
                <div className="flex-grow-1"/>
            <FilterSettings />
        </div>
    )
}
