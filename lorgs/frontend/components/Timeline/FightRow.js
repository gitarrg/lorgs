/* A row in our Timeline. representing a single Fight.

This basically just wraps a number of Boss/Player Rows.

*/

import * as constants from "./constants.js";
import PlayerRow from "./PlayerRow.js";
import filter_logic from "../../filter_logic.js";


export default class FightRow {

    constructor(fight_data) {

        this._visible = true

        // input data
        this.fight_data = fight_data
        this.duration = Math.ceil(fight_data.duration / 1000); // ms to s

        // Groups
        this.foreground = new Konva.Group()
        this.background = new Konva.Group()

        this.rows = [] // child rows

        // create child rows
        this.add_row(fight_data, fight_data.boss)
        fight_data.players.forEach(player => this.add_row(fight_data, player))

        this.layout_children()

    }

    add_row(fight_data, player_data) {

        if (!(player_data && player_data.name)) { return}

        const row = new PlayerRow(fight_data, player_data)
        this.rows.push(row)

        this.foreground.add(row.foreground)
        this.background.add(row.background)
    }

    layout_children() {

        let y = 0 // accumulate the height over time, to take into account visibility
        this.rows.forEach((row) => {
            row.y(y)
            y += row.height()
        })
    }

    //////////////////////////////
    // Attributes
    //
    visible(value) {

        if (value !== undefined) {
            this._visible = value
            this.rows.forEach(row => row.visible(value))
        }
        return this._visible
    }

    height() {
        const heights = this.rows.map(row => row.height())
        return heights.reduce((a, b) => a + b, 0)
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
    _handle_apply_filters_pre(filters) {
        const visible = filter_logic.is_fight_visible(this.fight_data, filters)
        this.visible(visible)
    }


    _handle_apply_filters_post() {
        this.layout_children()
    }

    handle_event(event_name, payload) {

        // apply filters to the fight itself (before processing children)
        if (event_name === constants.EVENT_APPLY_FILTERS ) { this._handle_apply_filters_pre(payload)}
        if (!this.visible()) { return }

        this.rows.forEach(row => row.handle_event(event_name, payload))

        // postprocess after filters applied (in case height change due to child rows updating)
        if (event_name === constants.EVENT_APPLY_FILTERS ) { this._handle_apply_filters_post()}
    }

    update_display_settings(settings) {
        this.rows.forEach(row => row.update_display_settings(settings))
        this.foreground.update_display_settings(settings)
    }
}
