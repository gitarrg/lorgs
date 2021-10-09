
import { createSlice } from '@reduxjs/toolkit'
import API from '../api.js'


////////////////////////////////////////////////////////////////////////////////
// Actions
//

export function get_roles(state) {

    return state.roles

    let roles = Object.values(state.roles)
    roles = roles.filter(role => role.id <= 1000) // filter out data roles
    return roles
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
        const roles = await API.load_roles()
        dispatch(set_roles(roles))
    }
}
