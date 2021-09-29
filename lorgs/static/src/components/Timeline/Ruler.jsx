
import React, { useState, useEffect } from "react";
import { Group, Rect, Line } from 'react-konva';

import "konva/lib/shapes/Rect"
import "konva/lib/shapes/Line"
import "konva/lib/shapes/Text"

import { LINE_HEIGHT} from "../../constants.jsx"

const TICK_DISTANCE = 10; // seconds
const TIMESTAMP_DISTANCE = 30;
const COLOR = "white";



function create_ticks(duration) {
    console.log("create_ticks", duration)

    let ticks = []
    for (let t = 0; t < duration; t += TICK_DISTANCE) {
    
        let big = (t % TIMESTAMP_DISTANCE) == 0;
        let h = big ? 10 : 5

        let tick = <Line 
            key={`ruler_line_${t}`}
            name={`ruler_line_${t}`}
            stroke="white"
            strokeWidth={0.5}
            points={[0.5, LINE_HEIGHT - h, 0.5, LINE_HEIGHT - 1]}
            transformsEnabled="position"
            x={t}
        />
        ticks.push(tick)
    }
    return ticks
}


export default function Ruler(props) {

    console.log("Ruler main")
    // let ticks = []

    const [ticks, setTicks] = React.useState([])

    React.useEffect(() => {
        console.log("Timeline Ruler Update Duration")
        let new_ticks = create_ticks(props.duration)
        setTicks(new_ticks)
    }, [props.duration])

    return (

        <Group>

            <Rect
                height={28}
                width={200}
                fill="green"
             />
             {ticks}

        </Group>

    )
}
