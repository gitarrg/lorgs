/* A row on the Timeline 

    this is the container for the casts if single boss or player.

*/

import Konva from "konva"

export default class ActorLane extends Konva.Group {

    constructor(stage, fight_data) {

        this.stage = stage
        this.fight_data = fight_data

        this.duration = fight_data.duration / 1000; // ms to s
        this.duration = Math.ceil(this.duration);

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
        // this.background = new Konva.Group()
        this.add(this.background_fill)
    }

    update() {

    }

}