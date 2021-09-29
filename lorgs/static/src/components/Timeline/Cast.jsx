

import React, { useContext } from 'react'
import { Group, Rect, Text } from 'react-konva';

import { LINE_HEIGHT, CONTEXT } from '../../constants.jsx';
import AppDataContext from "./../../AppDataContext.jsx"





export default class Cast extends React.Component {

    contextType = AppDataContext;
    
    constructor (props) {
        super(props);

        console.log("create cast", this.context)

        // const data = getAppData()
        // this.app_context = useContext(AppDataContext)
        const spell = this.context.spells[this.props.cast.id]
        if (!spell) { return}

        this.text = <Text
            ref={ref_text}
            text={toMMSS(this.props.cast.ts * 0.001)}
            x={27}
            fontSize={14}
            height={LINE_HEIGHT}
            verticalAlign='middle'
            fontFamily="Lato"
            fill="white"
            listening={false}
            transformsEnabled="position"
        />
               
    }
    
    update_scale() {
        if (ref_text.current) {
            ref_text.current.text()
        }
    }
    // React.useEffect(update_scale)
    
    render() {

        console.log("render Cast")
        return (
            <Group x={props.cast.ts * 0.001 * app_context.zoom}>
            <Rect 
                width={spell.duration * app_context.zoom}
                height={LINE_HEIGHT}
                fill={spell.color}
                listening={false}
            />
            {text}
        </Group>
        )
    }
}
