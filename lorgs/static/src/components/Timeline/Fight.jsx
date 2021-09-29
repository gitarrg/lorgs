

import React,  { useRef } from 'react'
import { Group, Rect } from 'react-konva';

import { LINE_HEIGHT} from "../../constants.jsx"
import Cast from './Cast.jsx';



// class FightBackground extends ReactKonva.Group {}


class Fight2 extends React.Component {


    constructor() {
        super()

        this.node = undefined;

        this.group = <Group></Group>

        console.log(this.group)

        this.background_fill = <Rect>
            height={LINE_HEIGHT}
            x={-0.5}
            y={0.5}
            fill="#222"
            stroke="black"
            strokeWidth={1}
            listening={false}
            transformsEnabled="position"
        </Rect>

        // this.group = <Group ref={node => (this.node = node)} />
        // console.log("group", this.group, this.node)
    }

    render() {
        return (
            this.group
        )
    }
}



export default function Fight(props) {

    const ref = useRef(null)

    const group = useRef(null)
    const background_fill = useRef(null)

    const player = props.player
    const fight = player.fight
    const scale = 2


    React.useEffect(() => {
        console.log("Fight Effect", group.current)

        group.current.y(props.player.rank * 28)

        let bg = background_fill.current
        // bg.fill("red")
        // bg.width(600)
        // bg.height(10)


    }, [])

    // props.player.casts = props.player.casts.slice(0, 2)

    return (
        <Group ref={group}>
            <Rect
                ref={background_fill}
                x={-0.5}
                y={0.5}
                height={28}
                width={props.player.fight.duration * 0.001 * scale}
                fill="#222"
                stroke="black"
                strokeWidth={1}
                listening={false}
                // transformsEnabled="position"
            ></Rect>

            {props.player.casts.map((cast, i) => (
                <Cast key={`cast_${i}`} cast={cast} />
            ))}

        </Group>
    )
}

