
import React from "react";
import { useSelector, useDispatch } from 'react-redux'

import * as constants from "./constants.js";
import Stage from "./Stage.js"
import { get_is_loading, MODES } from "../../store/ui.js";
import { get_fights } from "../../store/fights.js";
import TimelineTooltip from "./TimelineTooltip.jsx";


export default function TimelineCanvas() {


    //////////////////////////////////////
    // HOOKS
    //
    const dispatch = useDispatch()
    const ref = React.useRef() // container div for the canvas
    const stage_ref = React.useRef() // canvas itself

    // state vars
    const mode = useSelector(state => state.ui.mode)
    const is_loading = useSelector(state => get_is_loading(state))
    const fights_loading = useSelector(state => get_is_loading(state, "fights"))
    const spells_loading = useSelector(state => get_is_loading(state, "spells"))
    const fights = useSelector(state => get_fights(state))

    const ui_settings = useSelector(state => state.ui.settings)
    const spell_display = useSelector(state => state.spells.spell_display)
    const selected_spells = useSelector(state => state.spells.selected_spells)
    const filters = useSelector(state => state.ui.filters)

    //////////////////////////////////////
    // Listeners
    //

    // initial creation
    React.useEffect(() => {
        dispatch({type: "ui/set_loading", key: "stage", value: true})
        stage_ref.current = new Stage({container: ref.current})
    }, [])

    // Update: ui.mode
    React.useEffect(() => {
        stage_ref.current.FIGHT_SPACE = mode == MODES.SPEC_RANKING ? 0 : 10
    }, [mode])

    React.useEffect(() => {
        // not ready yet
        if (fights_loading || spells_loading) { return }
        stage_ref.current.set_fights(fights)
        stage_ref.current.handle_event(constants.EVENT_APPLY_FILTERS, filters)
        dispatch({type: "ui/set_loading", key: "stage", value: false})

    }, [fights_loading, spells_loading])

    React.useEffect(() => {

    }, [is_loading])

    // Pass trough UI Settings like "show_cooldown", "show_duration"
    React.useEffect(() => {
        stage_ref.current.handle_event(constants.EVENT_DISPLAY_SETTINGS, ui_settings)
    }, [ui_settings])

    // update spell visibility
    React.useEffect(() => {
        stage_ref.current.handle_event(constants.EVENT_SPELL_DISPLAY, spell_display)
    }, [spell_display])

    React.useEffect(() => {
        stage_ref.current.handle_event(constants.EVENT_SPELL_SELECTED, selected_spells)
    }, [selected_spells])

    React.useEffect(() => {
        stage_ref.current.handle_event(constants.EVENT_APPLY_FILTERS, filters)
    }, [filters])

    //////////////////////////////////////
    // Render
    //
    return (
        <div className="flex-grow-1 overflow-hidden">
            <div ref={ref} id="player_timelines_container"/>
            <TimelineTooltip />
        </div>
    )
}
