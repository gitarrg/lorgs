
import { createSlice } from '@reduxjs/toolkit'
import API from '../api.js'
import { group_spells_by_type } from './spells.js'


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

/** Find the first spec that can use a given spell
 * @param {object} state current state
 * @param {integer} spell_id id of the spell to find
 * @returns {object} the matched spell
*/
export function get_spec_for_spell_id(state, spell_id) {
    return Object.values(state.specs || {}).find(spec => {
        return Object.values(spec.spells_by_type || {}).some(spell_group => {
            return spell_group.includes(spell_id)
        }) // spell group
    }) // specs
}


////////////////////////////////////////////////////////////////////////////////
// Slice
//

function _process_spec(spec) {
    spec.loaded = false
    spec.icon_path = `/static/images/specs/${spec.full_name_slug}.jpg`
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

        set_spec_spells: (state, action) => {
            const {spec_slug, spells} = action.payload
            const spec = state[spec_slug]
            if (!spec) { return state}

            spec.spells_by_type =  group_spells_by_type(spells)
            spec.loaded = true
            return state
        },

    }, // reducers
})

export default SLICE.reducer


////////////////////////////////////////////////////////////////////////////////
// Extra Actions


export function load_specs() {

    return async dispatch => {
        dispatch({type: "ui/set_loading", key: "specs", value: true})
        const specs = await API.load_specs()
        dispatch(SLICE.actions.set_specs(specs))
        dispatch({type: "ui/set_loading", key: "specs", value: false})
    }
}


export function load_spec_spells(spec_slug) {

    return async dispatch => {
        const load_key = `specs/${spec_slug}`
        dispatch({type: "ui/set_loading", key: load_key, value: true})
        const spells = await API.load_spec_spells(spec_slug)

        dispatch(SLICE.actions.set_spec_spells({spec_slug, spells}))

        dispatch({type: "ui/set_loading", key: load_key, value: false})
    }
}
