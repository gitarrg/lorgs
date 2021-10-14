/* A row in our Timeline. representing a single Player or Boss.

Includes multiple elements for background, foreground etc, that can be
added to their representative layers on the stage.

Note:
    This is not a Konva Object but just a wrapper to direct multiple Groups at once.

*/

import Player from "./Player"
import PlayerRowBackground from "./PlayerRowBackground"
import filter_logic from "../../filter_logic";
import { EVENT_APPLY_FILTERS, LINE_HEIGHT } from "./constants";
import type Fight from "../../types/fight";
import type Actor from "../../types/actor";


export default class PlayerRow {

    duration: number
    foreground: Player
    background: PlayerRowBackground

    constructor(fight: Fight, player: Actor) {
        this.duration = Math.ceil(fight.duration / 1000); // ms to s

        // Groups
        this.foreground = new Player(this, player)
        this.background = new PlayerRowBackground(this)
    }

    //////////////////////////////
    // Attributes
    //

    visible(value? :boolean) {

        if (value !== undefined) {
            this.background.visible(value)
            this.foreground.visible(value)
        }
        return this.foreground.visible()
    }

    height() : number {
        return this.visible() ? LINE_HEIGHT : 0;
    }

    y(y: number) {
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

    _handle_apply_filters(filters: any) {
        const visible = filter_logic.is_player_visible(this.foreground.player_data, filters)
        this.visible(visible)
    }

    handle_event(event_name: string, payload: any) {
        if (event_name === EVENT_APPLY_FILTERS ) {
            this._handle_apply_filters(payload)
            if (!this.visible()) { return }
        }
        this.background.handle_event(event_name, payload)
        this.foreground.handle_event(event_name, payload)
    }
}
