import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import { createSelector } from 'reselect'
import type Role from '../types/role'
import { AppDispatch, RootState } from './store'
import { fetch_data } from '../api'
import { LOGO_URL } from '../constants'


////////////////////////////////////////////////////////////////////////////////
// Selectors
//

export function get_roles(state: RootState) {
    return state.roles
}


export const get_player_roles = createSelector<RootState, { [key: string]: Role }, Role[]>(
    get_roles,
    (roles_map ) => {
        const roles = Object.values(roles_map)
        return roles.filter(role => role.id < 1000)
    }
)


export function get_role(state: RootState, role_name: string) {
    return state.roles[role_name]
}


////////////////////////////////////////////////////////////////////////////////
// Slice
//

function create_placeholder_role(name: string, num_specs: number) {

    const specs = Array.from({length: num_specs}, (x, i) => `placeholder:${i}`)

    return {
        id: 0,
        code: name.toLowerCase(),
        name: name,
        specs: specs,
        icon_path: LOGO_URL,
    }
}


const INITIAL_STATE = {
    tank: create_placeholder_role("Tank", 6),
    heal: create_placeholder_role("Heal", 6),
    mdps: create_placeholder_role("MDPS", 13),
    rdps: create_placeholder_role("RDPS", 11),
}


const SLICE = createSlice({
    name: "roles",

    initialState: INITIAL_STATE as { [key: string]: Role },

    reducers: {
        set_roles: (state, action: PayloadAction<Role[]>) => {

            action.payload.forEach(role => {
                role.icon_path = `/static/img/roles/${role.code}.jpg`
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
