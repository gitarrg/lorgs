
import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import { fetch_data } from '../api'
import { AppDispatch } from './store'



const SLICE = createSlice({
    name: "status",

    initialState: {
        status: {}
    },

    reducers: {

        set_status: (state, action: PayloadAction<{}>) => {
            state.status = action.payload
            return state
        },
    },
})

export default SLICE.reducer

export const {
    set_status,
} = SLICE.actions


export function load_status() {

    return async (dispatch: AppDispatch) => {

        const url = "/api/status/spec_ranking";
        const data = await fetch_data(url);
        dispatch(set_status(data))
    } // dispatch
}
