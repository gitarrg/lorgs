
import Konva from "konva"

import * as constants from "./constants.js"


class TimelineMarker extends Konva.Group {

    color = "#db1212"
    color_hover = "#ed2828"
    color_drag = "#d9b84e"

    handle_width = 60
    handle_height = 20

    constructor(config={}) {
        config.draggable = true
        config.transformsEnabled = "position"
        config.name = "timeline_marker"
        super(config)

        // the time the marker is at. (in seconds)
        this.t = 0;

        this.line = new Konva.Line({
            name: "line",
            points: [0, 10, 0, 100],  // fix height
            stroke: this.color,
            strokeWidth: 2,
        })
        this.add(this.line)

        this.handle = new Konva.Rect({
            name: "handle",
            x: -this.handle_width/2,
            width: this.handle_width,
            height: this.handle_height,
            fill: this.color,
            cornerRadius: 3,
            listening: true,
            transformsEnabled: "position",
        })
        this.add(this.handle)

        this.label = new Konva.Text({
            name: "label",

            text: "",  // will be set in update()
            fontSize: 14,
            fontFamily: "Lato",
            fill: "white",
            transformsEnabled: "position",

            x: this.handle.x(),
            width: this.handle.width(),
            height: this.handle.height(),

            verticalAlign: 'middle',
            align: "center",
            listening: false,
        })
        this.add(this.label)
        this.on("dragmove", this.on_dragmove)

        this.on('mouseover', () => {this.hover(true)});
        this.on('mouseout', () => {this.hover(false)});

        this.on("mousedown contextmenu", (e) => {

            e.evt.preventDefault();
            if (e.evt.button === 2) {

                let stage = this.getStage()

                if (stage && stage.overlay_layer) {
                    console.log("removing marker")
                    this.remove()
                    stage.overlay_layer.batchDraw()
                }
            }


        })
    }

    //////////////////////////////
    //
    update() {

        let stage = this.getStage()
        if (!stage) { return }

        // update label
        this.label.text(toMMSS(this.t))

        // update position
        if (stage.zoom_changed) {
            this.x(this.t * stage.scale_x)
        }
    }

    set_height(height) {
        this.line.points([0, 10, 0, height]);
    }

    //////////////////////////////
    // EVENTS

    hover(state) {
        this.line.strokeWidth(state ? 5 : 2)
        const stage = this.getStage();
        if (!stage) { return }
        stage.container().style.cursor = state ? "w-resize" : "default";

        this.handle.fill(state ? this.color_hover : this.color)
        this.line.strokeWidth(state ? 4 : 2)
    }

    on_dragmove() {

        // constrain in Y
        this.y(0);

        // save the time the marker is at. (required for stage zoom)
        let stage = this.getStage()
        this.t = this.x() / stage.scale_x

        this.update()
    }
}


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

        this.duration = 1000; // time in seconds

        this.ticks = [];
        this.timestamps = [];

        this.markers = []


        this.mouse_crosshair_y = new Konva.Line({
            name: "mouse_crosshair_y",
            points: [0.5, constants.LINE_HEIGHT, 0.5, 999],  // fix height
            stroke: "white",
            strokeWidth: 0.5,
            fill: "white",
            transformsEnabled: "position",
            visible: false,
        })

        this.bbox = new Konva.Rect({
            height: constants.LINE_HEIGHT-2,
            width: 200,
            transformsEnabled: "none",
        })
        this.bbox.on("mouseover", () => {this.mouse_crosshair_y.visible(true)})
        this.bbox.on("mouseout", () => {this.mouse_crosshair_y.visible(false)})
        this.stage.on("mousemove", () => {this.update_crosshair()})

        this.stage.overlay_layer.add(this.bbox)
        this.stage.overlay_layer.add(this.mouse_crosshair_y)

        this.bbox.on("dblclick dbltap", () => this.add_marker())

    }

    create_ticks() {

        // reset
        this.destroyChildren()

        if (this.duration <= 0) {return;}

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
                    strokeScaleEnabled: false,
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

    update_duration(new_duration) {
        this.duration = new_duration;
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

        this.bbox.width(this.duration * scale_x)
        this.duration && this.cache()
        this.markers.forEach(marker => marker.update())
    }

    handle_event(event_name, payload) {
        if (event_name === constants.EVENT_ZOOM_CHANGE) { this._handle_zoom_change(payload)}
    }


    ////////////////////////////////////////////////////////////////////////////
    // Interaction
    //

    update_crosshair() {

        if (!this.mouse_crosshair_y.visible()) {return}

        let pointer = this.stage.getPointerPosition();
        if (!pointer) { return }

        this.mouse_crosshair_y.x(pointer.x - this.stage.x())
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
