
import React from "react";
import { useSelector } from 'react-redux'

import AppContext from "./../../AppContext/AppContext.jsx"
import Stage from "./Stage.js"

const PRINT_CANVAS_UPDATES = false


export default function TimelineCanvas(props) {


    const ctx = AppContext.getData()

    const ref = React.useRef() // container div for the canvas
    const stage_ref = React.useRef() // canvas itself

    // initial creation
    React.useEffect(() => {
        console.time("init canvas")
        
        // create the konva stage
        let stage = new Stage({container: ref.current})
        stage.FIGHT_SPACE = ctx.mode == AppContext.MODES.SPEC_RANKING ? 0 : 10
        stage_ref.current = stage

        console.timeEnd("init canvas")
        return
    }, [])


    React.useEffect(() => {
        const stage = stage_ref.current
        stage.set_spells(ctx.spells)
    }, [ctx.spells])

    // update when fights or filters get changed
    React.useEffect(() => {
        const stage = stage_ref.current
        PRINT_CANVAS_UPDATES && console.time("canvas: set fights")
        stage.set_fights(ctx.fights)
        PRINT_CANVAS_UPDATES && console.timeEnd("canvas: set fights")
        PRINT_CANVAS_UPDATES && console.time("canvas: create")
        stage.create()
        PRINT_CANVAS_UPDATES && console.timeEnd("canvas: create")
        PRINT_CANVAS_UPDATES && console.time("canvas: update")
        stage.update()
        stage.update_size()
        PRINT_CANVAS_UPDATES && console.timeEnd("canvas: update")

    }, [ctx.fights])


    // update when fights or filters get changed
    React.useEffect(() => {
        const stage = stage_ref.current
        PRINT_CANVAS_UPDATES && console.time("canvas update filters")
        stage.update()
        stage.update_size()
        PRINT_CANVAS_UPDATES && console.timeEnd("canvas update filters")
    }, [ctx.fights, ctx.filters])
    
    
    // update when fights or filters get changed
    React.useEffect(() => {
        console.log("redux filters changed")
        
        console.time("canvas update filters 2")
        const stage = stage_ref.current
        stage.schedule_update()
        stage.update_size()
        console.timeEnd("canvas update filters 2")
       
    }, [useSelector(state => state.filters)])
 
    const show_cooldown = useSelector(state => state.show_cooldown)
    const show_duration = useSelector(state => state.show_duration)
    const show_casttime = useSelector(state => state.show_casttime)
    React.useEffect(() => { stage_ref.current.toggle_cooldown(show_cooldown) }, [show_cooldown])
    React.useEffect(() => { stage_ref.current.toggle_duration(show_duration) }, [show_duration])
    React.useEffect(() => { stage_ref.current.toggle_casttime(show_casttime) }, [show_casttime])

    return (
        <div ref={ref} id="player_timelines_container" className="flex-grow-1" />
    )
}
