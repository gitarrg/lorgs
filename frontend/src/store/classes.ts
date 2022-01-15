import type Class from "../types/class"
import { AppDispatch, RootState } from "./store"
import { createSlice, PayloadAction } from "@reduxjs/toolkit"
import { fetch_data } from "../api"
import { sort_spell_types } from "./spells"


type ClassesSlice = {
    class_names: string[]
    classes: {[key: string]: Class}
}


////////////////////////////////////////////////////////////////////////////////
// Selectors

export function get_class_names(state: RootState) {
    return state.classes.class_names
}


export function get_class(state: RootState, class_name_slug: string) {
    return state.classes.classes[class_name_slug]
}


////////////////////////////////////////////////////////////////////////////////
// Slice

const INITIAL_STATE: ClassesSlice = {
    class_names: [],
    classes: {}
}


const SLICE = createSlice({

    name: "classes",
    initialState: INITIAL_STATE,

    reducers: {
        set_classes: (state, action: PayloadAction<{[key: string]: Class}>) => {

            state.classes = {}
            state.class_names = []
            
            Object.values(action.payload).forEach(wow_class => {
                wow_class.icon_path = `/static/img/classes/${wow_class.name_slug}.webp`

                state.class_names.push(wow_class.name_slug)
                state.classes[wow_class.name_slug] = wow_class
            });
            state.class_names = sort_spell_types(state.class_names)
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