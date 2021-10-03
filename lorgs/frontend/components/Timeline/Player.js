
import Cast from "./Cast.js"
import {LINE_HEIGHT} from "./../../constants.js"

export default class Player extends Konva.Group {

    constructor(stage, player_data) {
        super()
        this.stage = stage
        this.transformsEnabled("position")
        // this.casts_group = new Konva.Group()
        
        this.player_data = player_data

        // load casts
        this.casts = (player_data.casts || []).map(cast_data => new Cast(this.stage, cast_data))
        this.casts = this.casts.filter(cast => cast.spell)
        this.casts.forEach(cast => { cast.create() })

        // create background
        this.background_fill = new Konva.Rect({
            height: LINE_HEIGHT,
            width: 20,
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
    }

    update() {

        let visible = this.should_be_visible()
        this.visible(visible)
        this.background.visible(visible)
        if (!visible) {
            return
        }
        // this.stage.back_layer.add(this.background)

        this.casts.forEach(cast => {

            if (cast.spell && cast.spell.show) {

                cast.update()

                if (cast.getParent() == undefined) {
                    this.add(cast)
                }

                // move one after the other to the top/
                // assuming they are sorted by time.. this should fix overlaps
                cast.moveToTop()

            } else {
                if (cast.getParent() != undefined) {
                    cast.remove()
                }
            }
        })

        this.clearCache() // clear to make sure we update (even if eg: all children are hidden)
        if (this.hasChildren()) {
            this.cache()
        }
    }

    should_be_visible() {
        return this.player_data.visible !== false
    }
}
