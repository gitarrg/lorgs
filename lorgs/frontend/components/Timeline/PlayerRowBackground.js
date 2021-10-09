
import * as constants from "./constants.js"


export default class FightBackground extends Konva.Group {

    constructor(row) {
        super()

        this.row = row // parent row element

        // create background
        this.fill = new Konva.Rect({
            height: constants.LINE_HEIGHT,
            width: this.row.duration * constants.DEFAULT_ZOOM,
            x: -0.5,
            y: 0.5,
            fill: "#222",
            stroke: "black",
            strokeWidth: 1,
            listening: false,
            transformsEnabled: "position",
        })
        this.add(this.fill)
    }

    /////////////////////////
    // Events

    _handle_zoom_change(scale_x) {
        this.fill.width(this.row.duration * scale_x)
    }

    handle_event(event_name, payload) {
        if (event_name === constants.EVENT_ZOOM_CHANGE) { this._handle_zoom_change(payload)}


        this.width() && this.cache()

    }
}


