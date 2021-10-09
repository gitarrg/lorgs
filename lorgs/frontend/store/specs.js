
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

/* Find the first spec that can use a given spell */
export function get_spec_for_spell_id(state, spell_id) {
    return Object.values(state.specs).find(spec => {
        return Object.values(spec.spells_by_type).some(spell_group => {
            return spell_group.includes(spell_id)
        }) // spell group
    }) // specs
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
    }, // reducers

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


