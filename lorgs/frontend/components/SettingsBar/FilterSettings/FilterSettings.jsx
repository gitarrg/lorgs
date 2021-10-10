import React from 'react'

import ButtonGroup from '../shared/ButtonGroup.jsx'
import FilterCovenantGroup from './FilterCovenant.jsx'
import FilterKilltimeGroup from './FilterKilltime.jsx'


export default function FilterSettings({collapsed: collapsed_init=false}) {

    const [collapsed, setCollapsed] = React.useState(collapsed_init)

    function handle_click() {
        setCollapsed(!collapsed)
    }

    return (
        <>
            {!collapsed && <FilterCovenantGroup />}
            {!collapsed && <FilterKilltimeGroup />}

            <ButtonGroup name="Filters" side="right">
                <div onClick={handle_click} className="button icon-s rounded border-white fas fa-filter" data-tip="show/hide filters" />
            </ButtonGroup>

        </>
    )
}
