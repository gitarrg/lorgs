/*
    TODO:
        fix the triggers here

*/

import React from 'react'
import { useDispatch } from 'react-redux'
import { set_filter } from '../../../store/ui.js';
import ButtonGroup from '../shared/ButtonGroup.jsx';


const CHANGE_RATE = 5; // seconds to incr/decr per scroll event
const KEY_UP = "38"
const KEY_DOWN = "40"


function FilterKilltimeInput({name, start=0, placeholder="0:00" }) {

    //////////////////////////
    // Hooks
    //
    const ref = React.useRef(null);
    const [text, setText] = React.useState(null); // time as text
    const [seconds, setSeconds] = React.useState(start) // time in seconds
    const dispatch = useDispatch()

    //////////////////////////
    // Events
    //
    function handle_input() {
        setText(ref.current.value)

        const new_seconds = ref.current.value ? time_to_seconds(ref.current.value) : seconds
        if (new_seconds === undefined) { return} // invalid input
        setSeconds(new_seconds)
    }

    function update_seconds(change) {
        setSeconds(prev_value => Math.max(0, prev_value + change))
    }

    function handleWheel(event) {
        event.preventDefault();

        const change = CHANGE_RATE * (event.deltaY > 0 ? -1 : 1)
        update_seconds(change)
    }

    // setting "onWheel"-property had passive event listener issues
    React.useEffect(() => {
        const element = ref.current
        element.addEventListener("wheel", handleWheel);
        return () => {
            element.removeEventListener("wheel", handleWheel);
        };
    }, [])

    function handleKeyDown(event) {
        if (event.keyCode == KEY_UP)   { update_seconds(+CHANGE_RATE) }
        if (event.keyCode == KEY_DOWN) { update_seconds(-CHANGE_RATE) }
    }

    React.useEffect(() => {
        // update text whenever seconds get changed
        const new_text = seconds == start ? null : seconds_to_time(seconds, {padding: false})
        setText(new_text)

        dispatch(set_filter({ group: "killtime", name: name, value: seconds }))
    }, [seconds])


    //////////////////////////
    // Render
    //
    return (
        <input
            ref={ref}
            onChange={handle_input}
            onKeyDown={handleKeyDown}
            type="text"
            value={text || ""}
            className="form-control"
            placeholder={placeholder}
            pattern="\d+:\d{2}"
        />
    )
}



export default function FilterKilltimeGroup() {

    return (
        <ButtonGroup name="Killtime" side="right">
            <div className="input-group input-group-sm killtime_input">
                <FilterKilltimeInput name="min" placeholder="0:00" />
                <span className="input-group-text">-</span>
                <FilterKilltimeInput name="max" placeholder="9:00" start={9*60} />
            </div>
        </ButtonGroup>
    )
}
