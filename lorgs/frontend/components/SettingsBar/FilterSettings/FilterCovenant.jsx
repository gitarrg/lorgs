import React from 'react'
import { useSelector, useDispatch } from 'react-redux'

import FilterButton from '../shared/FilterButton.jsx'
import ButtonGroup from '../shared/ButtonGroup.jsx'



function FilterCovenantButton({covenant}) {

    const covenant_slug = covenant.toLowerCase()
    const dispatch = useDispatch()

    function onClick({value}) {

        dispatch({
            type: "update_filter",
            field: covenant_slug,
            value: !value
        })
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
