
import Konva from "konva"

import * as constants from "./constants.js"
import store from "./../../store/store.js"


function create_cast_cooldown(spell) {
    if (!spell.cooldown) { return }
    return new Konva.Rect({
        name: "cast_cooldown",
        width: spell.cooldown * constants.DEFAULT_ZOOM,
        height: constants.LINE_HEIGHT-1,
        fill: spell.color,
        opacity: 0.1,
        listening: false,
        transformsEnabled: "none",
        perfectDrawEnabled: false,
    })
}


function create_cast_duration(spell) {
    if (!spell.duration) { return }

    return new Konva.Rect({
        name: "cast_duration",
        width: spell.duration * constants.DEFAULT_ZOOM,
        height: constants.LINE_HEIGHT-1,
        fill: spell.color,
        listening: true,  // the fake bbox might be smaller
        opacity: 0.5,
        transformsEnabled: "none",
        perfectDrawEnabled: false,
    })
}

function create_cast_icon(spell) {

    // is the browser smart enough to not load the same image 100x?
    const image_obj = new Image();
    image_obj.src = spell.icon_path

    // create the konva image
    const icon = new Konva.Image({
        name: "cast_icon",
        image: image_obj,
        listening: false,
        x: 3.5, // padding
        y: 3.5, // padding
        width: 20,
        height: 20,
        stroke: "black",
        strokeWidth: 1,
        transformsEnabled: "position",
        perfectDrawEnabled: false,
    })

    icon.loading = image_obj.loading // custom flag to check is the img was loaded
    image_obj.onload = () => {
        icon.loading = false
    }

    return icon
}


function create_cast_text(cast) {
    return new Konva.Text({
        name: "cast_text",
        text: toMMSS(cast.timestamp),
        x: 27,
        y: 0,
        fontSize: 14,

        height: constants.LINE_HEIGHT,
        verticalAlign: 'middle',

        fontFamily: "Lato",
        fill: "white",
        listening: false,
        transformsEnabled: "position",
    })
}


export default class Cast extends Konva.Group {

    constructor(cast_data) {
        super()

        // Kova Attrs
        this.listening(true)
        this.transformsEnabled("position")
        this.name("Cast")

        // get redux store
        const state = store.getState()

        // Cast & Spell Info
        this.spell_id = cast_data.id;
        this.timestamp = cast_data.ts / 1000;
        this.spell = state.spells.all_spells[this.spell_id];

        // guess we are done here
        if (!this.spell) { return }

        // Internal Attrs
        this.hovering = false
        this.selected = false // cached value to avoid reading from redux all the time


        ////////////////////////////
        // create elements
        //
        this.cast_cooldown = create_cast_cooldown(this.spell)
        this.cast_cooldown && this.add(this.cast_cooldown)

        this.cast_duration = create_cast_duration(this.spell)
        this.cast_duration && this.add(this.cast_duration)

        this.cast_icon = create_cast_icon(this.spell)
        this.cast_icon && this.add(this.cast_icon)

        this.cast_text = create_cast_text(this)
        this.cast_text && this.add(this.cast_text)

        // invisible box for mouse events
        // (some casts might not have a duration-bar to use)
        this.mouse_event_bbox = new Konva.Rect({
            width: this.cast_text.width() + 3,
            height: constants.LINE_HEIGHT-1,
            listening: true,
        });
        this.add(this.mouse_event_bbox)

        this.visible(this.spell.show)
        this.y(1); // for the background stroke

        ////////////////////////////
        // Setup Events
        //
        this.mouse_event_bbox.on('mousedown', (e) => this.handle_mousedown(e));  // TODO: only on left click
        this.mouse_event_bbox.on('mouseover', () => {this.hover(true)});
        this.mouse_event_bbox.on('mouseout', () => {this.hover(false)});

        // prepare the tooltip content, as it doesn't change
        this.tooltip_content = `${this.spell.name}`
        this.tooltip_content += cast_data.counter ? ` #${cast_data.counter}` : ""
        this.tooltip_content += "<br>"
        this.tooltip_content += `${toMMSS(this.timestamp)}`
    }

    update_style() {

        if (!this.visible()) { return;}

        const stage = this.getStage()
        if (!stage) { return}

        // default state
        this.cast_text && this.cast_text.fontStyle("normal");
        this.cast_text && this.cast_text.fill("white");
        this.cast_duration && this.cast_duration.opacity(0.5)
        this.cast_cooldown && this.cast_cooldown.opacity(0.1)
        this.cast_icon && this.cast_icon.opacity(1.0)
        this.cast_icon && this.cast_icon.strokeWidth(1)
        this.opacity(1.0)

        if (stage.has_selection) {
            if (this.selected) {
                this.cast_text && this.cast_text.fontStyle("bold");
                this.cast_duration && this.cast_duration.opacity(0.85)
                this.cast_cooldown && this.cast_cooldown.opacity(0.4)
            } else {
                this.opacity(.5)
                this.cast_text && this.cast_text.fill("#ccc")
                this.cast_icon && this.cast_icon.opacity(0.5)
                this.cast_icon && this.cast_icon.strokeWidth(0)
            }
        }
        else if (this.hovering) {
            this.cast_duration && this.cast_duration.opacity(0.75)
            this.cast_cooldown && this.cast_cooldown.opacity(0.3)
        }
    }

    ////////////////////////////////////////////////////////////////////////////
    // Events
    //

    _handle_display_settings(settings) {
        this.cast_icon.visible(settings.show_casticon)
        this.cast_text.visible(settings.show_casttime)
        this.cast_cooldown && this.cast_cooldown.visible(settings.show_cooldown)
        this.cast_duration && this.cast_duration.visible(settings.show_duration)
    }

    _handle_zoom_change(scale_x) {
        this.x(scale_x * this.timestamp)
        this.cast_cooldown && this.cast_cooldown.width(this.spell.cooldown * scale_x)
        this.cast_duration && this.cast_duration.width(this.spell.duration * scale_x)
    }

    _handle_spell_display(payload) {
        const visible = payload[this.spell_id] !== false
        this.visible(visible)
    }

    _handle_spell_selected(payload) {
        this.selected = payload.includes(this.spell_id)
        this.update_style()
    }

    handle_event(event_name, payload) {

        if (event_name === constants.EVENT_SPELL_DISPLAY) {this._handle_spell_display(payload)}

        // FIXME: this causes issues when you unhide a spell, where it does not have the latest events applied.
        // if (!this.visible()) { return} // no need to process the following events
        if (event_name === constants.EVENT_ZOOM_CHANGE) {this._handle_zoom_change(payload)}
        if (event_name === constants.EVENT_DISPLAY_SETTINGS) (this._handle_display_settings(payload))
        if (event_name === constants.EVENT_SPELL_SELECTED) (this._handle_spell_selected(payload))
    }

    ////////////////////////////////////////////////////////////////////////////
    // Mouse Events
    //
    hover(hovering) {

        this.hovering = hovering;

        this.update_style()

        // update cursor
        const stage = this.getStage()
        stage.container().style.cursor = this.hovering ? "pointer" : "grab";
        stage.batchDraw()

        //////////////////
        // handle tooltip
        const position = this.absolutePosition()

        // add stage global position
        const container = stage.container()
        const container_position = container.getBoundingClientRect()
        position.x += container_position.x
        position.y += container_position.y

        position.x += this.cast_icon.x() + (this.cast_icon.width() / 2) // center above the icon
        store.dispatch({
            type: constants.EVENT_SHOW_TOOLTIP,
            payload: {
                content: this.hovering ? this.tooltip_content : "",
                position: position
            },
        })
    }

    select(event) {
        store.dispatch({
            type: constants.EVENT_SPELL_SELECTED,
            payload: {
                spell_id: this.spell_id,
                selected: !this.selected,
                deselect_others: !event.evt.ctrlKey,
            },
        })
    }

    handle_mousedown(event) {
        event.evt.preventDefault()

        if (event.evt.button == 0) {
            return this.select(event)
        }
    }
}
