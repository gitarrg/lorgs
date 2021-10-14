
import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import { fetch_data } from '../api'
import type Role from '../types/role'
import { AppDispatch, RootState } from './store'



////////////////////////////////////////////////////////////////////////////////
// Actions
//

export function get_roles(state: RootState) {
    return state.roles
}


export function get_role(state: RootState, role_name: string) {
    return state.roles[role_name]
}


////////////////////////////////////////////////////////////////////////////////
// Slice
//

const SLICE = createSlice({
    name: "roles",

    initialState: {} as { [key: string]: Role },

    reducers: {
        set_roles: (state, action: PayloadAction<Role[]>) => {

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

    return async (dispatch: AppDispatch) => {
        dispatch({type: "ui/set_loading", payload: {key: "roles", value: true}})

        // request
        let roles_map: { roles: Role[] } = await fetch_data("/api/roles")
        let roles = roles_map.roles // take array from dict
        roles.sort((a, b) => (a.id > b.id) ? 1 : -1  )

        dispatch(SLICE.actions.set_roles(roles))
        dispatch({type: "ui/set_loading", payload: {key: "roles", value: false}})
    }
}
