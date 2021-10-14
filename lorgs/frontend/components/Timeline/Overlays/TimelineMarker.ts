import Konva from "konva"

import * as constants from "../constants"
import type Stage from "../Stage"
import { toMMSS } from "../../../utils"


export default class TimelineMarker extends Konva.Group {

    #color = "#db1212"
    #color_hover = "#ed2828"

    #handle_width = 60
    #handle_height = 20

    // the time the marker is at. (in seconds)
    #time = 0

    /** The vertical Line */
    #line: Konva.Line

    /** Rectangle at the top that holds the Label */
    #handle: Konva.Rect

    /** Text inside the Handle */
    #label: Konva.Text


    constructor(config={}) {
        super(config)
        this.draggable(true)
        this.transformsEnabled("position")
        this.name("timeline_marker")

        // the time the marker is at. (in seconds)
        // this.#time = 0;

        this.#line = new Konva.Line({
            name: "line",
            points: [0, 10, 0, 100],  // fix height
            stroke: this.#color,
            strokeWidth: 2,
        })
        this.add(this.#line)

        this.#handle = new Konva.Rect({
            name: "handle",
            x: -this.#handle_width * 0.5,
            width: this.#handle_width,
            height: this.#handle_height,
            fill: this.#color,
            cornerRadius: 3,
            listening: true,
            transformsEnabled: "position",
        })
        this.add(this.#handle)

        this.#label = new Konva.Text({
            name: "label",

            text: "",  // will be set in update()
            fontSize: 14,
            fontFamily: "Lato",
            fill: "white",
            transformsEnabled: "position",

            x: this.#handle.x(),
            width: this.#handle.width(),
            height: this.#handle.height(),

            verticalAlign: 'middle',
            align: "center",
            listening: false,
        })
        this.add(this.#label)


        this.on("dragmove", this.#on_dragmove)
        this.on('mouseover', () => {this.#hover(true)});
        this.on('mouseout', () => {this.#hover(false)});

        this.on("mousedown contextmenu", (e) => {
            e.evt.preventDefault();
            if (e.evt.button === 2) {
                let stage = this.getStage() as Stage || null

                if (stage && stage.overlay_layer) {
                    console.log("removing marker")
                    this.remove()
                    stage.overlay_layer.batchDraw()
                }
            }
        })

        // initial refresh
        this.#on_dragmove()
    }

    //////////////////////////////
    //
    set_height(height: number) {
        this.#line.points([0, 10, 0, height]);
    }

    //////////////////////////////
    // EVENTS

    #hover(state: boolean) {
        this.#line.strokeWidth(state ? 5 : 2)
        const stage = this.getStage();
        if (!stage) { return }
        stage.container().style.cursor = state ? "w-resize" : "default";

        this.#handle.fill(state ? this.#color_hover : this.#color)
        this.#line.strokeWidth(state ? 4 : 2)
    }

    #on_dragmove() {

        // constrain in Y
        this.y(0);

        // save the time the marker is at. (required for stage zoom)
        let stage = this.getStage() as Stage || null
        this.#time = this.x() / (stage?.scale_x || constants.DEFAULT_ZOOM)

        // update label
        this.#label.text(toMMSS(this.#time))
    }

    #handle_zoom_change(scale_x: number) {
        this.x(this.#time * scale_x)
    }

    handle_event(event_name: string, payload: any) {
        if (event_name === constants.EVENT_ZOOM_CHANGE) { this.#handle_zoom_change(payload)}
    }
}
