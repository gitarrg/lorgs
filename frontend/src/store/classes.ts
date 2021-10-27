import type Class from "../types/class"
import { AppDispatch } from "./store"
import { createSlice, PayloadAction } from "@reduxjs/toolkit"
import { fetch_data } from "../api"


type ClassesSlice = {
    class_names: string[]
    classes: {[key: string]: Class}
}


const INITIAL_STATE: ClassesSlice = {
    class_names: [],
    classes: {}
}


const SLICE = createSlice({

    name: "classes",
    initialState: INITIAL_STATE,

    reducers: {
        set_classes: (state, action: PayloadAction<{[key: string]: Class}>) => {
            state.classes = action.payload
            return state
        },
    }, // reducers
})

export default SLICE.reducer


////////////////////////////////////////////////////////////////////////////////
// Extra Actions


export function load_classes() {

    return async (dispatch: AppDispatch) => {
        dispatch({type: "ui/set_loading", payload: {key: "classes", value: true}})

        // Request
        const repsonce = await fetch_data("/api/classes");
        dispatch(SLICE.actions.set_classes(repsonce))

        dispatch({type: "ui/set_loading", payload: {key: "classes", value: false}})
    }
}