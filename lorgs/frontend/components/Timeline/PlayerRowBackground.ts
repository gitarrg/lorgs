
import Konva from "konva"
import * as constants from "./constants"
import type PlayerRow from "./PlayerRow"


export default class PlayerRowBackground extends Konva.Group {

    row: PlayerRow
    fill: Konva.Rect

    constructor(row: PlayerRow) {
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

    _handle_zoom_change(scale_x: number) {
        this.fill.width(this.row.duration * scale_x)
    }

    handle_event(event_name: string, payload: any) {
        if (event_name === constants.EVENT_ZOOM_CHANGE) { this._handle_zoom_change(payload)}
        this.width() && this.cache()
    }
}
