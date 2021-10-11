/*
    Custom Tooltip Component.

    Reads content and position from the redux state,
    so we can easily feed it from anywhere inside the app.

    Once content is received we start a short timer,
    and how the tooltip with some delay.

    If the state changes in the meantime, the component gets dismounted,
    and should cancel the timer.

*/
import React from 'react'
import { useSelector } from 'react-redux'
import parse from 'html-react-parser';

import { get_tooltip } from '../../store/ui.js'


const TOOLTIP_DELAY = 500


export default function TimelineTooltip() {

    const tooltip = useSelector(state => get_tooltip(state))
    const ref = React.useRef()

    React.useEffect(() => {

        // no tooltip? no timer!
        if (!ref.current) { return }

        // create timer to show the tooltip after some delay
        const interval = setTimeout(() => {
            ref.current.style.display = "block";
        }, TOOLTIP_DELAY);
        return () => clearInterval(interval);
    }, [tooltip]);

    // no content to show? :/
    if (!tooltip.content) {
        return null;
    }

    /////////////////////////////////
    // Render
    //
    const tooltip_content = parse(tooltip.content)
    return (
        <div
            ref={ref}
            className="timeline_tooltip"
            style={{left: tooltip.position.x, top: tooltip.position.y, display: "None"}}
        >
            <div className="timeline_tooltip_content">{tooltip_content}</div>
            <div className="timeline_tooltip_arrow"></div>
        </div>
    )
}
