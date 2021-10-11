import React from 'react'
import { useDispatch } from 'react-redux'

import FilterButton from '../shared/FilterButton.jsx'
import ButtonGroup from '../shared/ButtonGroup.jsx'
import { set_filter } from '../../../store/ui.js'


function FilterCovenantButton({covenant}) {

    const covenant_slug = covenant.toLowerCase()
    const dispatch = useDispatch()

    function onClick({value}) {
        dispatch(set_filter({ group: "covenant", name: covenant_slug, value: value }))
    }

    return (
        <FilterButton
            key={covenant_slug}
            onClick={onClick}
            name={covenant_slug}
            full_name={covenant}
            icon_name={`covenants/${covenant_slug}`}
        />
    )
}


export default function FilterCovenantGroup() {
    return (
        <ButtonGroup side="right" name="Covenant">
            <FilterCovenantButton covenant="Kyrian" />
            <FilterCovenantButton covenant="Venthyr" />
            <FilterCovenantButton covenant="Nightfae" />
            <FilterCovenantButton covenant="Necrolord" />
        </ButtonGroup>
    )
}
