

import Konva from "konva"
import * as constants from "../constants"


export default class MouseCrosshair extends Konva.Line {

    constructor() {
        super({
            name: "mouse_crosshair_y",
            points: [0.5, constants.LINE_HEIGHT, 0.5, 999],  // fix height
            stroke: "white",
            strokeWidth: 0.5,
            fill: "white",
            transformsEnabled: "position",
            visible: false,
        })
        // last known pointer position in seconds on the timeline
        this.time = 0
    }

    _update_position() {
        const stage = this.getStage()
        this.x( this.time * stage.scale_x )
    }

    _handle_mousemove() {

        if (!this.visible()) {return}

        const stage = this.getStage()
        let pointer = stage.getPointerPosition();
        if (!pointer) { return }

        // store the time the mouse is at
        this.time = (pointer.x - stage.x()) / stage.scale_x
        this._update_position()
    }

    handle_event(event_name, payload) {
        if (event_name === constants.EVENT_ZOOM_CHANGE) { this._update_position()}
    }
}
