
import Cast from "./Cast.js"


export default class Player {

    constructor(stage, player_data) {

        this.stage = stage
        this.casts_group = new Konva.Group()
        this.casts_group.transformsEnabled("position")

        this.player_data = player_data

        // load casts
        this.casts = player_data.casts.map(cast_data => new Cast(this.stage, cast_data))
    }

    create() {
        this.casts = this.casts.filter(cast => cast.spell)
        this.casts.forEach(cast => { cast.create() })
    }

    update() {

        let visible = this.should_be_visible()
        this.casts_group.visible(visible)
        if (!visible) {
            return
        }

        this.casts.forEach(cast => {

            if (cast.spell && cast.spell.show) {

                cast.update()

                if (cast.getParent() == undefined) {
                    this.casts_group.add(cast)
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

        this.casts_group.clearCache() // clear to make sure we update (even if eg: all children are hidden)
        if (this.casts_group.hasChildren()) {
            this.casts_group.cache()
        }
    }

    should_be_visible() {
        return this.player_data.visible !== false
    }

}
