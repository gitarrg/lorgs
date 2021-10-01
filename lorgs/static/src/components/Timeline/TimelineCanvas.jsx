
import React from "react";

import AppContext from "./../../AppContext/AppContext.jsx"
import Stage from "./Stage.js"


export default function TimelineCanvas(props) {


    const ctx = AppContext.getData()

    const ref = React.useRef() // container div for the canvas
    const stage_ref = React.useRef() // canvas itself

    // initial creation
    React.useEffect(() => {
        console.time("init canvas")
        
        // create the konva stage
        let stage = new Stage({container: ref.current})
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
        console.time("canvas: set fights")
        stage.set_fights(ctx.fights)
        console.timeEnd("canvas: set fights")
        console.time("canvas: create")
        stage.create()
        console.timeEnd("canvas: create")
        console.time("canvas: update")
        stage.update()
        stage.update_size()
        console.timeEnd("canvas: update")

    }, [ctx.fights])


    // update when fights or filters get changed
    React.useEffect(() => {
        const stage = stage_ref.current
        console.time("canvas update filters")
        stage.update()
        stage.update_size()
        console.timeEnd("canvas update filters")
    }, [ctx.fights, ctx.filters])


    React.useEffect(() => { stage_ref.current.toggle_cooldown(ctx.show_cooldown) }, [ctx.show_cooldown])
    React.useEffect(() => { stage_ref.current.toggle_duration(ctx.show_duration) }, [ctx.show_duration])
    React.useEffect(() => { stage_ref.current.toggle_casttime(ctx.show_casttime) }, [ctx.show_casttime])

    return (
        <div ref={ref} id="player_timelines_container" className="flex-grow-1" />
    )
}
