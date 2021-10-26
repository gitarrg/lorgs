

import Konva from "konva"
import * as constants from "../constants"
import Stage from "../Stage"


export default class MouseCrosshair extends Konva.Line {

    // last known pointer position in seconds on the timeline
    private time = 0

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
    }

    private update_position() {
        const stage = this.getStage() as Stage || null
        this.x( this.time * (stage?.scale_x  || constants.DEFAULT_ZOOM ))
    }

    handle_mousemove() {

        if (!this.visible()) {return}

        const stage = this.getStage() as Stage || null
        if (!stage) { return }
        let pointer = stage.getPointerPosition();
        if (!pointer) { return }

        // store the time the mouse is at
        this.time = (pointer.x - stage.x()) / stage.scale_x
        this.update_position()
    }

    handle_event(event_name: string, _: any) {
        if (event_name === constants.EVENT_ZOOM_CHANGE) { this.update_position()}
    }
}
