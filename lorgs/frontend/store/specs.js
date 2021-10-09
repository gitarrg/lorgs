
import { createSlice } from '@reduxjs/toolkit'
import API from '../api.js'


////////////////////////////////////////////////////////////////////////////////
// Actions
//

export function get_specs(state) {
    return Object.values(state.specs)
}

export function get_spec(state, spec_slug="") {
    spec_slug = spec_slug || state.ui.spec_slug // input or current spec
    return state.specs[spec_slug]
}


////////////////////////////////////////////////////////////////////////////////
// Slice
//

function _process_spec(spec) {

    spec.icon_path = `/static/images/specs/${spec.full_name_slug}.jpg`
    spec.spells_by_type = spec.spells || {}
    return spec
}


const SLICE = createSlice({
    name: "specs",

    initialState: {},

    reducers: {

        set_specs: (state, action) => {

            action.payload.forEach(spec => {
                state[spec.full_name_slug] = _process_spec(spec)
            })
            return state
        },

        set_spec: (state, action) => {
            const spec = action.payload
            state[spec.full_name_slug] = _process_spec(spec)
            return state
        }


    },
})

export const { set_specs, set_spec } = SLICE.actions
export default SLICE.reducer


////////////////////////////////////////////////////////////////////////////////
// Extra Actions


export function load_specs() {

    return async dispatch => {
        const specs = await API.load_specs()
        dispatch(set_specs(specs))
    }
}

export function load_spec(spec_slug) {

    return async dispatch => {
        const spec = await API.load_spec(spec_slug)
        dispatch(set_spec(spec))
    }
}


