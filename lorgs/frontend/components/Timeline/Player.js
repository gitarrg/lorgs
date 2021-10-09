
import Cast from "./Cast.js"
import * as constants from "./constants.js"


export default class Player extends Konva.Group {

    constructor(row, player_data) {
        super()
        this.row = row
        this.transformsEnabled("position")

        this.clip({
            x: 0,
            y: 1,
            width: this.row.duration * constants.DEFAULT_ZOOM,
            height: constants.LINE_HEIGHT,
        })

        this.player_data = player_data

        // load casts
        this.casts = (player_data.casts || []).map(cast_data => new Cast(cast_data))
        this.casts = this.casts.filter(cast => cast.spell)

        this.layout_children()
    }


    layout_children() {

        this.casts.forEach(cast => {

             if (cast.spell && cast.visible()) {

                // add cast if its not added yet
                if (cast.getParent() == undefined) {
                    this.add(cast)
                }

                // move one after the other to the top/
                // assuming they are sorted by time.. this should fix overlaps
                cast.moveToTop()

            } else { // dont show

                // remove cast if its currently added
                if (cast.getParent() != undefined) {
                    cast.remove()
                }
            }
        })
    }

    schedule_cache() {

        this.clearCache() // clear to make sure we update (even if eg: all children are hidden)
        if (this.hasChildren()) {
            this.cache() // TODO: add throttle?
        }
        return

        console.log("schedule_cache")

        if (this.schedule_cache_timer) {
            // console.log("schedule_cache -- > clear")
            return
            //clearTimeout(this.schedule_cache_timer)
        }

        this.clearCache() // clear to make sure we update (even if eg: all children are hidden)
        console.log("schedule_cache -- > create")
        this.schedule_cache_timer = setTimeout(() => {
            // fixme: breaks hover(again)
            console.log("schedule_cache -- > run")
            if (this.hasChildren()) {
                this.cache() // TODO: add throttle?
            }
            this.schedule_cache_timer = undefined
        }, 1000)
    }

    //////////////////////////////
    // Events
    //

    _handle_spell_display() {
        this.layout_children()
    }

    _handle_zoom_change(scale_x) {
        this.clipWidth(this.row.duration * scale_x)
    }

    handle_event(event_name, payload) {
        if (event_name === constants.EVENT_ZOOM_CHANGE) { this._handle_zoom_change(payload)}
        this.casts.forEach(cast => cast.handle_event(event_name, payload))

        // after cast update, so we can handle the cast visibility in there
        if (event_name === constants.EVENT_SPELL_DISPLAY) {this._handle_spell_display(payload)}

        this.schedule_cache()
    }
}
