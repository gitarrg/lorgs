
import Konva from "konva"

import {LINE_HEIGHT} from "./../../constants.js"



export default class Fight extends Konva.Group {

    constructor(stage, fight_data) {
        super()
        this.name("Fight")
        // this.listening(true)
        this.transformsEnabled("position")

        this.stage = stage
        this.fight_data = fight_data

        this.duration = fight_data.duration / 1000; // ms to s
        this.duration = Math.ceil(this.duration);

        this.actors = []
        this.clip({
            x: 0,
            y: 1,
            width: 200,
            height: LINE_HEIGHT,
        })

        this.background_fill = new Konva.Rect({
            height: LINE_HEIGHT,
            // width: 20,
            x: -0.5,
            y: 0.5,
            fill: "#222",
            stroke: "black",
            strokeWidth: 1,
            listening: false,
            transformsEnabled: "position",
        })
        this.background = new Konva.Group()
        this.background.name("fight_background")
        this.background.add(this.background_fill)
        // this.add(this.background)
    }

    create() {
        this.actors.forEach((actor, i) => {
            actor.create();
            this.add(actor.casts_group);
        })
    }

    update() {

        // update visibility
        let visible = this.should_be_visible()
        this.visible(visible)
        this.background.visible(visible)
        if (!visible) {return}


        let w = this.duration * this.stage.scale_x;
        w = Math.floor(w); // avoid drawing strokes on half pixels

        // update background
        this.background_fill.width(w)
        this.clipWidth(w-1) // clip content to show background stroke

        // update actors
        this.actors.forEach(actor => {actor.update()})

        // reflect changes to the background layer
        // this.background.visible(this.visible())
        // this.background.y(this.y())
    }

    should_be_visible() {

        if (this.fight_data.visible === false) {
            return false
        }

        return this.actors.some(actor => actor.should_be_visible())
    }


}

