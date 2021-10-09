/* Loads Constant Data from the API that is used on all pages. */

import React from 'react'
import { useDispatch } from 'react-redux'

import { load_bosses } from "../store/bosses.js"
import { load_specs } from "../store/specs.js"
import { load_roles } from "../store/roles.js"



export default function GlobalDataLoader() {

    const dispatch = useDispatch()

    React.useEffect(() => {
        console.log("loading global data")
        dispatch(load_bosses())
        dispatch(load_roles())
        dispatch(load_specs())
    }, [])

    return null
}

