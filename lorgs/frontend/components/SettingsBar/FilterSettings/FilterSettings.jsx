


import React from 'react'

import ButtonGroup from '../shared/ButtonGroup.jsx'
import FilterCovenant from './FilterCovenant.jsx'
import FilterKilltime from './FilterKilltime.jsx'



export default function FilterSettings({collapsed: collapsed_init=false}) {

    const [collapsed, setCollapsed] = React.useState(collapsed_init)

    const content = !collapsed && <>
        <ButtonGroup side="right" name="Covenant">
            <FilterCovenant covenant="Kyrian" />
            <FilterCovenant covenant="Venthyr" />
            <FilterCovenant covenant="Nightfae" />
            <FilterCovenant covenant="Necrolord" />
        </ButtonGroup>

        <ButtonGroup name="Killtime" side="right">
            <FilterKilltime />
        </ButtonGroup>
    </>

    function handle_click() {
        setCollapsed(!collapsed)
    }

    return (
        <>
            {content}

            <ButtonGroup name="Filters" side="right">
                <div onClick={handle_click} className="button icon-s rounded border-white fas fa-filter" data-bs-toggle="tooltip" title="filter" />
            </ButtonGroup>

        </>
    )
}
