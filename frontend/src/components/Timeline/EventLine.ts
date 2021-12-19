
import * as constants from "./constants"
import Actor from "../../types/actor"
import Konva from "konva"
import store from "./../../store/store"
import type Event from "../../types/event"
import type Stage from "./Stage"
import { toMMSS } from "../../utils"


const ICON_ROOT = "https://wow.zamimg.com/images/wow/icons/small"


export default class EventLine extends Konva.Group {

    player_data: Actor
    event_data: Event

    timestamp: number
    tooltip_content: string

    line: Konva.Line
    label: Konva.Text
    mouse_event_bbox: Konva.Rect

    constructor(player_data: Actor, event_data: Event) {
        super()

        // Kova Attrs
        this.listening(true)
        this.transformsEnabled("position")

        // Attributes
        this.player_data = player_data
        this.event_data = event_data
        this.timestamp = event_data.ts / 1000

        // Elements
        this.line = new Konva.Line({
            points: [0, 0, 0, constants.LINE_HEIGHT],
            stroke: this.color,
            strokeWidth: 2,
            transformsEnabled: "none",
        })
        this.add(this.line)

        this.label = new Konva.Text({
            name: "cast_text",
            text: this._get_text_label(),
            fontSize: 14,

            x: 3, // gap between line and label

            height: constants.LINE_HEIGHT,
            verticalAlign: 'middle',

            fontFamily: "Lato",
            fill: this.color,
            listening: false,
            transformsEnabled: "position",
        })
        this.add(this.label)

        this.tooltip_content = this._get_text_tooltip()

        // invisible box for mouse events
        this.mouse_event_bbox = new Konva.Rect({
            width: this.label.width() + 3,
            height: constants.LINE_HEIGHT - 1,
            listening: true,
        });
        this.add(this.mouse_event_bbox)


        if (this.tooltip_content) {
            this.listening(true)
            this.mouse_event_bbox.on('mouseover', () => {this.hover(true)});
            this.mouse_event_bbox.on('mouseout', () => {this.hover(false)});
        }
    }

    get color() {
        return "#ccc"
    }

    _get_text_label() {
        return toMMSS(this.timestamp)
    }

    /** Tooltip Text Helpers */
    _get_tooltip_elements() {

        const items : any = {}
        const ed = this.event_data

        items["time"] = toMMSS(this.timestamp)

        // 18px is the native size of the "small"-images
        items["icon"]   = ed.spell_icon    ? `<img src="${ICON_ROOT}/${ed.spell_icon}" width="18px" height="auto">` : ""
        items["source"] = ed.source_name   ? `<span class=wow-${ed.source_class}>${ed.source_name}</span>` : ""
        items["spell"]  = ed.spell_name    ? `<span class=wow-boss>${ed.spell_name}</span>` : ""
        items["player"] = this.player_data ? `<span class="wow-${this.player_data.class}">${this.player_data.name}</span>` : ""

        return items
    }

    _get_tooltip_spell_name() {
        if (!this.event_data.spell_name) { return "" }
        return `<span class=wow-boss>${this.event_data.spell_name}</span>`
    }

    _get_text_player() {
        return `<span class="wow-${this.player_data.class}">${this.player_data.name}</span>`
    }

    _get_text_tooltip() {
        return ""
    }

    _handle_zoom_change(scale_x: number) {
        this.x(scale_x * this.timestamp)
    }

    handle_event(event_name: string, payload: any) {
        if (event_name === constants.EVENT_ZOOM_CHANGE) { this._handle_zoom_change(payload)}
    }

    hover(hovering: boolean) {

        // no tooltip
        if (!this.tooltip_content) { return }

        const stage = this.getStage() as Stage | null
        if (!stage) { return }

        const position = this.absolutePosition()
        // add stage global position
        const container = stage.container()
        const container_position = container.getBoundingClientRect()
        position.x += container_position.x
        position.y += container_position.y

        store.dispatch({
            type: constants.EVENT_SHOW_TOOLTIP,
            payload: {
                content: hovering ? this.tooltip_content : "",
                position: position
            },
        })
    }
}
