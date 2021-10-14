
import Konva from "konva"
import { toMMSS } from "../../utils";

import * as constants from "./constants"
import MouseCrosshair from "./Overlays/MouseCrosshair";
import TimelineMarker from "./Overlays/TimelineMarker";


export default class Ruler extends Konva.Group {

    tick_distance = 10; // seconds
    timestamp_distance = 30;
    color = "white";
    height = constants.LINE_HEIGHT;

    constructor(stage, config={}) {
        // config.listening = false
        config.transformsEnabled = "none"
        config.name = "Ruler"
        super(config)

        this.stage = stage

        this.duration = 0; // time in seconds
        this.ticks = [];
        this.timestamps = [];
        this.markers = []

        //////////////////////////
        // bbox used to catch mouse events
        this.bbox = new Konva.Rect({
            height: constants.LINE_HEIGHT-2,
            width: 200, // fixed in handle-zoom
            transformsEnabled: "none",
        })
        this.stage.overlay_layer.add(this.bbox)

        //////////////////////////
        // MouseCrosshair
        this.mouse_crosshair = new MouseCrosshair()
        this.bbox.on("mouseover", () => {this.mouse_crosshair.visible(true)})
        this.bbox.on("mouseout", () => {this.mouse_crosshair.visible(false)})
        this.bbox.on("mousemove", () => {this._handle_mousemove()})
        this.stage.overlay_layer.add(this.mouse_crosshair)

        //////////////////////////
        //
        this.bbox.on("dblclick dbltap", () => this.add_marker())

    }

    create_ticks() {

        // reset
        this.destroyChildren()

        if (this.duration <= 0) {return;}

        this.bottom_line = new Konva.Line({
            name: "bottom_line",
            points: [], // applied in handle_zoom
            stroke: "black",
            strokeWidth: 0.5,
            transformsEnabled: "none",
        })
        this.add(this.bottom_line)

        /////////////////////////////////////
        // create ticks
        //
        for (var t=0; t<this.duration; t+=this.tick_distance) {

            let big = (t % this.timestamp_distance) == 0;
            let h = big ? 10 : 5

            let tick = new Konva.Line({
                name: "tick",
                points: [0.5, constants.LINE_HEIGHT-h, 0.5, constants.LINE_HEIGHT-1],
                stroke: this.color,
                strokeWidth: 1,
                transformsEnabled: "position",
            })
            this.add(tick)

            if (big) {
                let text = new Konva.Text({
                    text: toMMSS(t),
                    name: "timestamp",
                    y: -10,
                    fontSize: 14,
                    height: constants.LINE_HEIGHT,
                    verticalAlign: 'bottom',
                    align: "center",
                    fontFamily: "Lato",
                    fill: this.color,
                    transformsEnabled: "position",
                })

                text.on("transform", () => {
                    console.log("update text")
                    text.scaleX(1.0)
                })
                this.add(text)
            } // if big
        } // for t
    }


    ///////////////////////////////////////////////////////////
    //

    update_duration(duration) {
        this.duration = duration;
        this.create_ticks()
    }

    update() {
        if (this.duration <= 0) {return;}
        this.update_crosshair()
    }

    ////////////////////////////////////////////////////////////////////////////
    // Events
    //
    _handle_zoom_change(scale_x) {

        // update ticks
        this.find(".tick").forEach((tick, i) => {
            tick.x(this.tick_distance * i * scale_x);
        })

        // update timestamps
        this.find(".timestamp").forEach((timestamp, i) => {
            let x = this.timestamp_distance * i * scale_x
            x += i==0 ? 0 : -18;
            timestamp.x(x)
        })

        this.bottom_line && this.bottom_line.points([0, constants.LINE_HEIGHT-0.5, this.duration * scale_x, constants.LINE_HEIGHT-0.5])

        this.bbox.width(this.duration * scale_x)
        this.duration && this.cache()
        // this.markers.forEach(marker => marker.update())
    }

    handle_event(event_name, payload) {
        if (event_name === constants.EVENT_ZOOM_CHANGE) { this._handle_zoom_change(payload)}

        this.mouse_crosshair.handle_event(event_name, payload)
        this.markers.forEach(marker => marker.handle_event(event_name, payload))
    }

    ////////////////////////////////////////////////////////////////////////////
    // Interaction
    //

    _handle_mousemove() {
        this.mouse_crosshair._handle_mousemove()
        this.stage.overlay_layer.batchDraw()
    }

    add_marker() {

        let pointer = this.stage.getPointerPosition();
        let x = pointer.x - this.stage.x()

        let marker = new TimelineMarker()
        marker.x(x);
        marker.set_height(this.stage.height())

        this.markers.push(marker)
        this.stage.overlay_layer.add(marker)

        // refresh the timestamp
        marker.on_dragmove()
    }
}
