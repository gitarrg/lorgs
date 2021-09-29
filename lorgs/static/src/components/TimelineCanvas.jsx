
// import { Stage, Layer } from 'react-konva';

import Ruler from "./Timeline/Ruler.js"
// import Fight from './Timeline/Fight.jsx';
// import { LINE_HEIGHT } from '../../timeline_modules/vars.js';

import AppDataContext from "./../AppDataContext.jsx"
import React from "react";


import Stage from "./Timeline/Stage.js"


export default function TimelineCanvas(props) {

    // console.log("TimelineCanvas main", props.duration)
    // let ruler = <Ruler key="TimelineRuler" duration={props.duration}/>

    const app_context = React.useContext(AppDataContext)

    const ref = React.useRef()

    // const scale = 2
    // const h = (props.players.length+1) * LINE_HEIGHT
    // const w = Math.max(...props.players.map(player => player.fight.duration/1000), 0);

    // initial creation
    React.useEffect(() => {
        console.log("init canvas", ref.current)

        // create the konva stage
        let stage = new Stage({container: ref.current})
        stage.create()
        stage.update()

        stage.print_tree()

    }, [])


    return (
        <div ref={ref} id="player_timelines_container" className="flex-grow-1" />
    )
}