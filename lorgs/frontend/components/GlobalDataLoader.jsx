/* Loads Constant Data from the API that is used on all pages. */

import React from 'react'
import { useDispatch } from 'react-redux'

import { load_bosses } from "../store/bosses.js"
import { load_specs } from "../store/specs.js"
import { load_roles } from "../store/roles.js"
import { load_spells } from '../store/spells.js'


export default function GlobalDataLoader() {

    const dispatch = useDispatch()

    React.useEffect(() => {
        console.log("loading global data")
        dispatch(load_bosses())
        dispatch(load_roles())
        dispatch(load_specs())

        // right now this always loads all spells.
        // should maybe filter by groups again
        dispatch(load_spells())

    }, [])

    return null
}

