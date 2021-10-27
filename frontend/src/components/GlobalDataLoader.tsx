/* Loads Constant Data from the API that is used on all pages. */

import { useEffect } from 'react'
import { useDispatch } from 'react-redux'

import { load_bosses } from "../store/bosses"
import { load_classes } from '../store/classes'
import { load_roles } from "../store/roles"
import { load_specs } from "../store/specs"


export default function GlobalDataLoader() {

    const dispatch = useDispatch()

    useEffect(() => {
        console.log("loading global data")
        dispatch(load_bosses())
        dispatch(load_classes())
        dispatch(load_roles())
        dispatch(load_specs())
    }, [])

    return null
}

