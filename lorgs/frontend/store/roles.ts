
import { createSlice } from '@reduxjs/toolkit'
import { fetch_data } from '../api'
import Role from '../types/role'



interface RolesSliceState {
    [key: string]: Role
}


////////////////////////////////////////////////////////////////////////////////
// Actions
//

export function get_roles(state) : RolesSliceState {
    return state.roles
}


export function get_role(state, role_name: string) : Role {
    return state.roles[role_name]
}


////////////////////////////////////////////////////////////////////////////////
// Slice
//

const SLICE = createSlice({
    name: "roles",

    initialState: {} as RolesSliceState,

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

export default SLICE.reducer


////////////////////////////////////////////////////////////////////////////////
// Extra Actions


export function load_roles() {

    return async dispatch => {
        dispatch({type: "ui/set_loading", key: "roles", value: true})

        // request
        let roles = await fetch_data("/api/roles")
        roles = roles.roles // take array from dict
        roles.sort((a, b) => (a.id > b.id) ? 1 : -1  )

        dispatch(SLICE.actions.set_roles(roles))
        dispatch({type: "ui/set_loading", key: "roles", value: false})
    }
}
