/* A row in our Timeline. representing a single Player or Boss.

Includes multiple elements for background, foreground etc, that can be
added to their representative layers on the stage.

Note:
    This is not a Konva Object but just a wrapper to direct multiple Groups at once.

*/

import Player from "./Player.js"
import PlayerRowBackground from "./PlayerRowBackground.js"
import filter_logic from "../../filter_logic.js";
import { EVENT_APPLY_FILTERS, LINE_HEIGHT } from "./constants.js";


export default class PlayerRow {

    constructor(fight_data, player_data) {
        this.duration = Math.ceil(fight_data.duration / 1000); // ms to s

        // Groups
        this.foreground = new Player(this, player_data)
        this.background = new PlayerRowBackground(this)
    }

    //////////////////////////////
    // Attributes
    //

    visible(val) {

        if (val !== undefined) {
            this.background.visible(val)
            this.foreground.visible(val)
        }
        return this.foreground.visible()
    }

    height() {
        return this.visible() ? LINE_HEIGHT : 0;
    }

    y(y) {
        // forward changes y-coord changes to both children
        this.background.y(y)
        this.foreground.y(y)
    }

    destroy() {
        this.background.destroy()
        this.foreground.destroy()
    }

    //////////////////////////////
    // Methods
    //

    _handle_apply_filters(filters) {
        const visible = filter_logic.is_player_visible(this.foreground.player_data, filters)
        this.visible(visible)
    }

    handle_event(event_name, payload) {
        if (event_name === EVENT_APPLY_FILTERS ) {
            this._handle_apply_filters(payload)
            if (!this.visible()) { return }
        }
        this.background.handle_event(event_name, payload)
        this.foreground.handle_event(event_name, payload)
    }

    update_display_settings(settings) {
        this.foreground.update_display_settings(settings)
    }
}
