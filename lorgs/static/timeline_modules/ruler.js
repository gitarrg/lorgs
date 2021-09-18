
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
            points: [0, 10, 0, 999],  // fix height
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
        // this.cast_duration.perfectDrawEnabled(false);
        this.add(this.handle)


        this.label = new Konva.Text({
            name: "label",

            // text: toMMSS(0),
            fontSize: 14,
            fontFamily: "Lato",
            fill: "white",
            transformsEnabled: "position",
            // y: -10,
            x: this.handle.x(),
            width: this.handle.width(),
            height: this.handle.height(),

            verticalAlign: 'middle',
            align: "center",

            // listening: false,
        })
        this.add(this.label)
        this.on("dragmove", this.on_dragmove)

        this.on('mouseover', () => {this.hover(true)});
        this.on('mouseout', () => {this.hover(false)});

        this.on("mousedown", (e) => {

            e.evt.preventDefault();
            if (e.evt.button === 2) {
                console.log("right clicked a marker")
                this.remove()
            }
        })
    }

    //////////////////////////////
    //
    update() {

        // update label
        let stage = this.getStage()
        const x = this.t; // / stage.scale_x;
        this.label.text(toMMSS(this.t))

        if (stage.zoom_changed) {
            this.x(this.t * stage.scale_x)
        }

    }

    //////////////////////////////
    // EVENTS

    hover(state) {
        this.line.strokeWidth(state ? 5 : 2)
        const stage = this.getStage();
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



class TimelineRuler extends Konva.Group {

    tick_distance = 10; // seconds
    timestamp_distance = 30;
    color = "white";
    height = LINE_HEIGHT;

    constructor(stage, config={}) {
        // config.listening = false
        config.transformsEnabled = "none"
        config.name = "TimelineRuler"
        super(config)

        this.stage = stage

        this.duration = 1000; // time in seconds

        this.ticks = [];
        this.timestamps = [];

        this.markers = []

        // const tick_sm = new Konva.Line({
        //     name: "ruler_tick",
        //     points: [0, 0, 0, height],
        //     stroke: "red",
        //     strokeWidth: 3,
        // })


        this.mouse_crosshair_y = new Konva.Line({
            name: "mouse_crosshair_y",
            points: [0.5, LINE_HEIGHT, 0.5, 999],  // fix height
            stroke: "white",
            strokeWidth: 0.5,
            fill: "white",
            transformsEnabled: "position",
        })

        this.bbox = new Konva.Rect({
            height: LINE_HEIGHT,
            width: 200,
            // stroke: "red",
            // strokeWidth: 1,
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
        this.ticks = [];
        this.timestamps = [];

        if (this.duration <= 0) {return;}

        /////////////////////////////////////
        // create ticks
        //
        for (var t=0; t<this.duration; t+=this.tick_distance) {

            let big = (t % this.timestamp_distance) == 0;
            let h = big ? 10 : 5

            let tick = new Konva.Line({
                name: "tick",
                points: [0.5, LINE_HEIGHT-h, 0.5, LINE_HEIGHT-1],
                stroke: this.color,
                strokeWidth: 1,
                transformsEnabled: "position",
            })

            // let tick = (big ? tick_lg : tick_sm).clone()
            this.ticks.push(tick)
            this.add(tick)

            if (big) {
                let text = new Konva.Text({
                    text: toMMSS(t),
                    name: "timestamp",
                    // x: 27,
                    y: -10,
                    fontSize: 14,
                    height: LINE_HEIGHT,
                    verticalAlign: 'bottom',
                    align: "center",
                    fontFamily: "Lato",
                    fill: this.color,
                    transformsEnabled: "position",
                    // listening: false,
                })
                this.timestamps.push(text)
                this.add(text)
            } // if big
        } // for t
        this.cache()
    }


    create() {
        this.stage = this.getStage()
        this.create_ticks()
    }


    update() {
        if (this.duration <= 0) {return;}


        if (this.stage.zoom_changed) {

            // update ticks
            this.find(".tick").forEach((tick, i) => {
                tick.x(this.tick_distance * i * this.stage.scale_x);
            })

            // update timestamps
            this.find(".timestamp").forEach((timestamp, i) => {
                let x = this.timestamp_distance * i * this.stage.scale_x
                x += i==0 ? 0 : -18;
                timestamp.x(x)
            })

            this.cache()
            this.bbox.width(this.duration * this.stage.scale_x)

            this.markers.forEach(marker => marker.update())


        }
    }

    ////////////////////////////////////////////////////////////////////////////
    // Interaction

    update_crosshair() {

        if (this) {
            let pointer = this.stage.getPointerPosition();

            // console.log("mousemove", pointer)
            this.mouse_crosshair_y.x(pointer.x - this.stage.x())
        }
    }

    add_marker() {

        let pointer = this.stage.getPointerPosition();
        let x = pointer.x - this.stage.x()

        let marker = new TimelineMarker()
        this.markers.push(marker)
        marker.x(x);
        this.stage.overlay_layer.add(marker)

        // refresh the timestamp
        marker.on_dragmove()
    }
}






