import { useState } from 'react'

import ButtonGroup from '../shared/ButtonGroup'
import FaButton from '../shared/FaButton'
import FilterCovenantGroup from './FilterCovenant'
import FilterKilltimeGroup from './FilterKilltime'


export default function FilterSettings({collapsed: collapsed_init=false}) {

    const [collapsed, setCollapsed] = useState(collapsed_init)

    function handle_click() {
        setCollapsed(!collapsed)
    }

    return (
        <>
            {!collapsed && <FilterCovenantGroup />}
            {!collapsed && <FilterKilltimeGroup />}

            <ButtonGroup name="Filters" side="right">
                <FaButton icon_name="fas fa-filter" onClick={handle_click} disabled={collapsed} />
            </ButtonGroup>

        </>
    )
}
