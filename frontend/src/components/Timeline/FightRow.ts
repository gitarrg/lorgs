/* A row in our Timeline. representing a single Fight.

This basically just wraps a number of Boss/Player Rows.

*/

import * as constants from "./constants";
import Konva from "konva";
import PlayerRow from "./PlayerRow";
import filter_logic from "../../filter_logic";
import type Actor from "../../types/actor";
import type Fight from "../../types/fight";
import { FilterValues } from "../../store/ui";
import { toMMSS } from "../../utils";


export default class FightRow {

    /* offset for the killtime text */
    KILLTIME_MARGIN = 5

    duration: number
    _visible: boolean
    _fight_data: Fight

    foreground: Konva.Group
    background: Konva.Group
    rows: PlayerRow[]
    killtime_text: Konva.Text


    constructor(fight_data: Fight) {

        this._visible = true

        // input data
        this._fight_data = fight_data
        this.duration = Math.ceil(fight_data.duration / 1000); // ms to s

        // Groups
        this.foreground = new Konva.Group()
        this.background = new Konva.Group()

        this.rows = [] // child rows

        // create child rows
        fight_data.boss && this.add_row(fight_data, fight_data.boss)
        fight_data.players.forEach(player => this.add_row(fight_data, player))

        this.killtime_text = this.create_killtime_text()
        this.foreground.add(this.killtime_text)

        this.layout_children()

    }

    add_row(fight: Fight, player: Actor) {

        if (!(player?.name)) { return}

        const row = new PlayerRow(fight, player)
        this.rows.push(row)

        this.foreground.add(row.foreground)
        this.background.add(row.background)
    }

    create_killtime_text() {

        return new Konva.Text({
            name: "cast_text",
            text: toMMSS(this.duration),
            x: this.KILLTIME_MARGIN + (this.duration * constants.DEFAULT_ZOOM) ,
            y: 0,
            fontSize: 14,

            height: constants.LINE_HEIGHT,
            verticalAlign: 'middle',

            fontFamily: "Lato",
            fill: "#999",
            listening: false,
            transformsEnabled: "position",
        })
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
    visible(value?: boolean) {

        if (value !== undefined) {
            this._visible = value
            this.rows.forEach(row => row.visible(value))
            this.killtime_text.visible(value)
        }
        return this._visible
    }

    height() : number {
        const heights = this.rows.map(row => row.height())
        return heights.reduce((a, b) => a + b, 0)
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

    _handle_zoom_change(scale_x: number) {
        this.killtime_text.x(this.KILLTIME_MARGIN + (this.duration * scale_x))
    }

    _handle_apply_filters_pre(filters: FilterValues) {
        const visible = filter_logic.is_fight_visible(this._fight_data, filters)
        this.visible(visible)
    }


    _handle_apply_filters_post() {
        this.layout_children()
    }

    handle_event(event_name: string, payload: any) {

        // apply filters to the fight itself (before processing children)
        if (event_name === constants.EVENT_APPLY_FILTERS ) { this._handle_apply_filters_pre(payload)}
        if (!this.visible()) { return }

        if (event_name === constants.EVENT_ZOOM_CHANGE) { this._handle_zoom_change(payload)}
        this.rows.forEach(row => row.handle_event(event_name, payload))

        // postprocess after filters applied (in case height change due to child rows updating)
        if (event_name === constants.EVENT_APPLY_FILTERS ) { this._handle_apply_filters_post()}
    }
}
