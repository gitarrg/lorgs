
import * as constants from "./constants"
import Konva from "konva"
import type DeathType from "../../types/death"
import { toMMSS } from "../../utils"
import store from "./../../store/store"
import type Stage from "./Stage"
import Actor from "../../types/actor"


// TMP
const ICON_ROOT = "https://wow.zamimg.com/images/wow/icons/small"

export default class Death extends Konva.Group {

    timestamp: number
    tooltip_content: string

    line: Konva.Line
    label: Konva.Text
    mouse_event_bbox: Konva.Rect

    COLOR = "#ff4d4d"

    constructor(player_data: Actor, death_data: DeathType) {
        super()

        // Kova Attrs
        this.listening(true)
        this.transformsEnabled("position")
        this.name("Death")

        // Attributes
        this.timestamp = death_data.ts

        // Elements
        this.line = new Konva.Line({
            points: [0, 0, 0, constants.LINE_HEIGHT],
            stroke: this.COLOR,
            strokeWidth: 2,
            transformsEnabled: "none",
        })
        this.add(this.line)
        
        this.label = new Konva.Text({
            name: "cast_text",
            text: "💀" + toMMSS(this.timestamp),
            x: 20,
            y: 1,
            fontSize: 14,
            
            height: constants.LINE_HEIGHT,
            verticalAlign: 'middle',
            
            fontFamily: "Lato",
            fill: this.COLOR,
            listening: false,
            transformsEnabled: "none",
        })
        this.add(this.label)

        // invisible box for mouse events
        // (some casts might not have a duration-bar to use)
        this.mouse_event_bbox = new Konva.Rect({
            width: this.label.width() + 3,
            height: constants.LINE_HEIGHT-1,
            listening: true,
        });
        this.add(this.mouse_event_bbox)
        this.mouse_event_bbox.on('mouseover', () => {this.hover(true)});
        this.mouse_event_bbox.on('mouseout', () => {this.hover(false)});



        // 18px is the native size of the "small"-images
        const tooltip_icon = death_data.icon && `<img src="${ICON_ROOT}/${death_data.icon}" width="18px" height="auto"> `
        const tooltip_name = death_data.name && ` from ${death_data.name}`
        this.tooltip_content = ""
        this.tooltip_content += `${tooltip_icon}${toMMSS(this.timestamp)}`
        this.tooltip_content += ` <span class="wow-${player_data.class}">${player_data.name}</span> dies${tooltip_name}.`

    }

    _handle_zoom_change(scale_x: number) {
        this.x(scale_x * this.timestamp)
    }

    handle_event(event_name: string, payload: any) {
        if (event_name === constants.EVENT_ZOOM_CHANGE) { this._handle_zoom_change(payload)}
    }

    hover(hovering: boolean) {

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
