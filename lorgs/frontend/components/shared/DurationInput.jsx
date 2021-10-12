import React from 'react'


const CHANGE_RATE = 5; // seconds to incr/decr per scroll event
const KEY_UP = "38"
const KEY_DOWN = "40"


/**
 * Component to input a short duration (up to 60min'sch)
 * Allows changing the value via input text, mousewheel and up/down keys.
 *
 * @param {integer} start initial value
 * @param {string} placeholder text to be shown as placeholder when the input is empty
 * @param {function} onChange Function that will be called with the seconds as first input
 *
 * @returns {ReactComponent} <input>
 */
export default function DurationInput({start, placeholder="0:00", onChange}) {

    ////////////////////////////////////////////////////////////////////////////
    // Hooks
    //
    const ref = React.useRef(null);
    const [text, setText] = React.useState(null); // time as text
    const [seconds, setSeconds] = React.useState(start) // time in seconds


    // helper to adjust the value of seconds by a given amount
    function update_seconds(change) {
        setSeconds(prev_value => Math.max(0, (prev_value || 0) + change))
    }

    ////////////////////////////////////////////////////////////////////////////
    // Events
    //

    /////////////////////////////////
    // Change via Text Input
    //   we always update our internal text-state
    //   and then additionally attempt to convert it into seconds
    function handle_input() {
        // update the current text value
        setText(ref.current.value)

        // user deleted the text
        if (ref.current.value === "") {
            return setSeconds(undefined)
        }

        // try to convert the text into seconds
        const new_seconds = time_to_seconds(ref.current.value)
        if (new_seconds === undefined) { return} // invalid input

        setSeconds(new_seconds)
    }

    /////////////////////////////////
    // Change via Mouse wheel
    //

    // callback for the mousewheeel
    function handleWheel(event) {
        event.preventDefault(); // prevent the regular page scrolling

        const change = CHANGE_RATE * (event.deltaY > 0 ? -1 : 1) // determine if we scroll up or down
        update_seconds(change)
    }

    // hook up the listeners
    // setting "onWheel" as a property had passive event listener issues
    React.useEffect(() => {
        const element = ref.current
        element.addEventListener("wheel", handleWheel);
        return () => {
            element.removeEventListener("wheel", handleWheel);
        };
    }, [])

    /////////////////////////////////
    // Change via Arrow Keys
    //
    function handleKeyDown(event) {
        if (event.keyCode == KEY_UP)   { update_seconds(+CHANGE_RATE) }
        if (event.keyCode == KEY_DOWN) { update_seconds(-CHANGE_RATE) }
    }


    /////////////////////////////////
    // Forward changes from any of the listeners above
    //
    React.useEffect(() => {
        // don't update the text whenever we have some empty string
        if (seconds !== undefined) {
            // update text so the user can see the current value,
            // when modifying the value via mouse wheel or keyboard
            const new_text = seconds_to_time(seconds, {padding: false})
            setText(new_text)
        }

        // forward result to any callbacks
        onChange && onChange(seconds)
    }, [seconds])


    ////////////////////////////////////////////////////////////////////////////
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
