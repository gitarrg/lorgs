
import React from "react";

import AppDataContext from "./../AppDataContext.jsx"
import Stage from "./Timeline/Stage.js"



export default function TimelineCanvas(props) {


    const ctx = React.useContext(AppDataContext)

    const ref = React.useRef() // container div for the canvas
    const stage_ref = React.useRef() // canvas itself

    // const scale = 2
    // const h = (props.players.length+1) * LINE_HEIGHT
    // const w = Math.max(...props.players.map(player => player.fight.duration/1000), 0);

    // initial creation
    React.useEffect(() => {
        console.log("init canvas", ref.current, ctx)

        // create the konva stage
        let stage = new Stage({container: ref.current})
        stage_ref.current = stage
        return
    }, [])

    // update once spells/fights are loaded
    React.useEffect(() => {
        const stage = stage_ref.current
        if (!stage) {return}
        if (ctx.spells.length == 0) {return}
        if (ctx.fights.length == 0) {return}


        console.log("update canvas", ctx)

        stage.set_spells(ctx.spells)
        stage.set_fights(ctx.fights)

        stage.create()
        stage.update()
        stage.update_size()

    }, [ctx.fights, ctx.spells])


    return (
        <div ref={ref} id="player_timelines_container" className="flex-grow-1" />
    )
}