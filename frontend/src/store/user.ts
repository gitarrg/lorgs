/** Slice to hold and request data about the currently logged in user. */
import jwt_decode from "jwt-decode";
import type { RootState, AppDispatch } from './store'
import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import { fetch_data } from '../api'


/** name of the local storage key we use to store the logged in user */
const LOCAL_STORAGE_KEY = "user_token"


/** Get the currently logged in user */
export function get_current_user(state: RootState) {
    return state.user
}


interface UserSliceState {

    logged_in: boolean
    name: string
    id: string
    permissions: string[],

    error?: string
    error_message?: string
}


const INITIAL_STATE: UserSliceState = {
    logged_in: false,
    name: "",
    id: "",
    permissions: []
}


const SLICE = createSlice({
    name: "user",

    initialState: INITIAL_STATE,

    reducers: {

        /** Store a newly received token */
        token_received: (state, action: PayloadAction<string>) => {
            localStorage.setItem(LOCAL_STORAGE_KEY, action.payload)
            return state
        },

        /** Read the User Data from a token */
        token_loaded: (state, action: PayloadAction<string>) => {
            const user_info: {} = jwt_decode(action.payload)
            return {
                ...state,
                ...user_info,
                logged_in: true,
            }
        },

        /** Store Error Inforation from a failed token request */
        token_failed: (state, action: PayloadAction<{error: "", message: ""}>) => {
            return {
                ...INITIAL_STATE,
                error: action.payload.error,
                error_message: action.payload.message,
            }
        },

        /** Log the user out of Lorrgs */
        logout: () => {
            localStorage.removeItem(LOCAL_STORAGE_KEY)
            return INITIAL_STATE
        },
    }, // reducers
})

export const {
    logout
} = SLICE.actions


export default SLICE.reducer


/** log the user into Lorrgs via a auth-code recieved from a third party Auth Provider */
export function login(code: string) {

    return async (dispatch: AppDispatch) => {

        // Request
        const repsonce = await fetch_data("/api/auth/token", {code});

        const token = repsonce.token
        if (token) {
            dispatch(SLICE.actions.token_received(token))
            dispatch(SLICE.actions.token_loaded(token))
        } else {
            dispatch(SLICE.actions.token_failed(repsonce))
        }
    }
}


/** load a previously logged in user  */
export function load_user() {

    return async (dispatch: AppDispatch) => {

        const token = localStorage.getItem(LOCAL_STORAGE_KEY) || ""
        if (!token) { return }
        dispatch(SLICE.actions.token_loaded(token))
    }
}
