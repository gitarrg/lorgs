/* A row in our Timeline. representing a single Player or Boss.

Includes multiple elements for background, foreground etc, that can be
added to their representative layers on the stage.

Note:
    This is not a Konva Object but just a wrapper to direct multiple Groups at once.

*/

import PlayerRowBackground from "./PlayerRowBackground.js"
import Player from "./Player.js"
import { LINE_HEIGHT } from "./constants.js";


export default class PlayerRow {

    constructor(fight_data, player_data) {

        // input data
        this.duration = Math.ceil(fight_data.duration / 1000); // ms to s

        // Groups
        this.foreground = new Player(this, player_data)
        this.background = new PlayerRowBackground(this)
    }

    //////////////////////////////
    // Attributes
    //

    height() {
        return LINE_HEIGHT;
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
    handle_event(event_name, payload) {
        this.background.handle_event(event_name, payload)
        this.foreground.handle_event(event_name, payload)
    }

    update_display_settings(settings) {
        this.foreground.update_display_settings(settings)
    }
}
