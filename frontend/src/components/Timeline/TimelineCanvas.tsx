import * as constants from "./constants";
import Stage from "./Stage"
import TimelineTooltip from "./TimelineTooltip";
import { get_fights } from "../../store/fights";
import { get_is_loading, MODES } from "../../store/ui";
import { useAppSelector } from "../../store/store_hooks";
import { useRef, useEffect} from "react";


export default function TimelineCanvas() {


    //////////////////////////////////////
    // HOOKS
    //
    const ref = useRef<HTMLDivElement>(null) // container div for the canvas
    const stage_ref = useRef<Stage>() // canvas itself

    // state vars
    const mode = useAppSelector(state => state.ui.mode)
    const is_loading = useAppSelector(get_is_loading)
    const fights = useAppSelector(get_fights)
    const ui_settings = useAppSelector(state => state.ui.settings)
    const spell_display = useAppSelector(state => state.spells.spell_display)
    const selected_spells = useAppSelector(state => state.spells.selected_spells)
    const filters = useAppSelector(state => state.ui.filters)

    //////////////////////////////////////
    // Listeners
    //

    // initial creation
    useEffect(() => {
        // dispatch({type: "ui/set_loading", key: "stage", value: true})
        if (!ref.current) { return }
        stage_ref.current = new Stage({container: ref.current})
    }, [])

    // Update: ui.mode
    useEffect(() => {
        stage_ref.current!.MODE = mode
    }, [mode])

    useEffect(() => {
        if (is_loading) { return } // not ready yet

        console.log("creating canvas", is_loading)
        stage_ref.current!.set_fights(fights)
        stage_ref.current!.handle_event(constants.EVENT_APPLY_FILTERS, filters)
    }, [is_loading])

    // Pass trough UI Settings like "show_cooldown", "show_duration"
    useEffect(() => {
        stage_ref.current!.handle_event(constants.EVENT_DISPLAY_SETTINGS, ui_settings)
    }, [ui_settings])

    // update spell visibility
    useEffect(() => {
        stage_ref.current!.handle_event(constants.EVENT_SPELL_DISPLAY, spell_display)
    }, [spell_display])

    useEffect(() => {
        stage_ref.current!.handle_event(constants.EVENT_SPELL_SELECTED, selected_spells)
    }, [selected_spells])

    useEffect(() => {
        stage_ref.current!.handle_event(constants.EVENT_APPLY_FILTERS, filters)
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
