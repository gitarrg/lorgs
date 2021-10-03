
import Konva from "konva"

import {LINE_HEIGHT} from "./../../constants.js"
import ActorLane from "./ActorLane.js"
import Player from "./Player.js"



export default class Fight extends Konva.Group {

    constructor(stage, fight_data) {
        super()
        this.name("Fight")
        // this.listening(true)
        this.transformsEnabled("position")

        this.stage = stage
        this.fight_data = fight_data

        this.total_height = 0
        this.duration = fight_data.duration / 1000; // ms to s
        this.duration = Math.ceil(this.duration);

        this.actors = []

        // TODO: add some [...map]-magic
        if (fight_data.boss) {
            this.actors.push(new Player(this.stage, fight_data.boss))
        }
        
        fight_data.players.forEach(player => {
            this.actors.push(new Player(this.stage, player))
        })

        this.clip({
            x: 0,
            y: 1,
            width: 200,
            height: LINE_HEIGHT,
        })
    }

    create() {
        this.actors.forEach((actor, i) => {
            actor.create();
            this.add(actor);
        })
    }

    update() {

        // update visibility
        let visible = this.should_be_visible()
        this.visible(visible)
        if (!visible) {return}

        this.stage.main_layer.add(this)

        let w = this.duration * this.stage.scale_x;
        w = Math.floor(w); // avoid drawing strokes on half pixels

        // update background
        this.clipWidth(w-1) // clip content to show background stroke
        
        // update actors
        let y = 0
        this.actors.forEach(actor => {
            // todo: check vis
            actor.update()
            
            if (actor.should_be_visible()) {
                actor.y(y)
                actor.background.y(y + this.y())
                actor.background_fill.width(w)
                y += LINE_HEIGHT
            }
        })
        this.clipHeight(y)
        this.height(y)

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

