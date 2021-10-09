/* A row in our Timeline. representing a single Fight.

This basically just wraps a number of Boss/Player Rows.

*/

import { LINE_HEIGHT } from "./constants.js";
import PlayerRow from "./PlayerRow.js";


export default class FightRow {

    constructor(fight_data) {

        // input data
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

        this.rows.forEach((row, i) => {
            row.y(i * LINE_HEIGHT)
        })
    }

    //////////////////////////////
    // Attributes
    //

    height() {

        return this.rows.length * LINE_HEIGHT;
        // return this.background.height();
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
        this.rows.forEach(row => row.handle_event(event_name, payload))
    }

    update_display_settings(settings) {
        this.rows.forEach(row => row.update_display_settings(settings))
        // this.foreground.update_display_settings(settings)
    }
}
