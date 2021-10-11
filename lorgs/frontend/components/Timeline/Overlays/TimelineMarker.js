
import * as constants from "../constants.js"


export default class TimelineMarker extends Konva.Group {

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
        this.time = 0;

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
    update_label() {
        // update label
        this.label.text(toMMSS(this.time))
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
        this.time = this.x() / stage.scale_x

        this.update_label()
    }


    _handle_zoom_change(scale_x) {
        this.x(this.time * scale_x)
    }

    handle_event(event_name, payload) {
        if (event_name === constants.EVENT_ZOOM_CHANGE) { this._handle_zoom_change(payload)}
    }

}
