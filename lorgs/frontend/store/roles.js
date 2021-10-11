
import { createSlice } from '@reduxjs/toolkit'
import API from '../api.js'


////////////////////////////////////////////////////////////////////////////////
// Actions
//

export function get_roles(state) {
    return state.roles
}


export function get_role(state, role_name) {
    return state.roles[role_name]
}


////////////////////////////////////////////////////////////////////////////////
// Slice
//


const SLICE = createSlice({
    name: "roles",

    initialState: {},

    reducers: {
        set_roles: (state, action) => {

            action.payload.forEach(role => {
                role.icon_path = `/static/images/roles/${role.code}.jpg`
                state[role.code] = role
            })
            return state
        },
    },
})


export const { set_roles } = SLICE.actions
export default SLICE.reducer


////////////////////////////////////////////////////////////////////////////////
// Extra Actions


export function load_roles() {

    return async dispatch => {
        dispatch({type: "ui/set_loading", key: "roles", value: true})
        const roles = await API.load_roles()
        dispatch(set_roles(roles))
        dispatch({type: "ui/set_loading", key: "roles", value: false})
    }
}
