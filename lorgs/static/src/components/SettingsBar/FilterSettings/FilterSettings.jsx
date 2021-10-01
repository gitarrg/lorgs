


import React from 'react'

import ButtonGroup from '../shared/ButtonGroup.jsx'
import FilterCovenant from './FilterCovenant.jsx'



export default function FilterSettings() {
    return (
        <div>
            <ButtonGroup name="Covenant">
                <FilterCovenant covenant="Kyrian" />
                <FilterCovenant covenant="Venthyr" />
                <FilterCovenant covenant="Nightfae" />
                <FilterCovenant covenant="Necrolord" />
            </ButtonGroup>
        </div>
    )
}
