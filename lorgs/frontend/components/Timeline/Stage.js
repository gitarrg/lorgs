import Konva from "konva"


import Ruler from "./Ruler.js"
import Spell from "./Spell.js"
import PlayerRow from "./PlayerRow.js";
import * as constants from "./constants.js";


// for performance
Konva.autoDrawEnabled = false;


export default class Stage extends Konva.Stage{

    ZOOM_RATE = 1.1
    ZOOM_MIN = 0.5

    THROTTLE = 200 // max update rate in ms

    FIGHT_SPACE = 10 // distance between fights in pixels


    constructor(options) {
        options.draggable = true
        options.strokeScaleEnabled = false
        super(options);

        /////////////////////////////////
        // custom attributes
        this.scale_x = 4;
        this.spells = {}
        this.rows = []

        // bool: true if any spell is selected
        this.has_selection = false;

        // bool: used to indicate if objects need to be rescaled
        this.zoom_changed = true; // true for initial load

        ////////////////////////////////
        // create layers
        this.back_layer = new Konva.Layer({listening: false})
        this.add(this.back_layer);

        this.main_layer = new Konva.Layer()
        this.add(this.main_layer);

        this.overlay_layer = new Konva.Layer()
        this.add(this.overlay_layer);

        // this.debug_layer = new Konva.Layer()
        // this.add(this.debug_layer);

        this.ruler = new Ruler(this);
        this.back_layer.add(this.ruler)

        // update canvas on window resize
        this.on("dragmove",  this.on_dragmove)
        this.on("wheel",  this.on_wheel)
        this.on("contextmenu", this.contextmenu)
    }

    ////////////////////////////////////////////////////////////////////////////
    // Attributes
    //

    has_values() {
        if (this.fights.length == 0) { return false}
        if (Object.keys(this.spells).length == 0) { return false}

        return true;
    }

    ////////////////////////////////////////////////////////////////////////////
    // CREATION AND DRAW
    //
    update_width() {
        this.width(this.longest_fight * this.scale_x)
        this.batchDraw()
    }

    update_display_settings(settings) {
        this.rows.forEach(row => row.update_display_settings(settings))
    }

    layout_children() {

        let y = this.ruler.height-1;

        this.rows.forEach(row => {
            row.y(y)
            y += row.height() + this.FIGHT_SPACE  // TODO: add FightRow that can have subrows
        })

        this.height(y)
    }

    ////////////////////////////////////////////////////////////////////////////
    // EVENTS
    //

    contextmenu(event) {
        event.evt.preventDefault();
    }

    _limit_movement() {
        this.y(0);
        this.x(Math.min(this.x(), 0))
    }

    on_dragmove() {
        this._limit_movement()
        this.batchDraw();
    }

    on_wheel(event) {

        // only zoom on shift/ctrl + scroll
        if (! (event.evt.shiftKey || event.evt.ctrlKey)) { return;}
        event.evt.preventDefault();

        ////////////////////////////////////
        // update scale

        let pointer = this.getPointerPosition();

        let old_offset = ( pointer.x - this.x()) / this.scale_x; // normalized distance between 0:00 and cursor

        this.scale_x = event.evt.deltaY < 0 ? this.scale_x * this.ZOOM_RATE : this.scale_x / this.ZOOM_RATE;
        this.scale_x = Math.max(this.scale_x, this.ZOOM_MIN)

        let new_offset = (old_offset * this.scale_x); // distance between 0:00 and cursor (new scale)
        let new_x = pointer.x - new_offset;

        this.x(new_x);
        this._limit_movement()

        ////////////////////////////////////
        // update scale
        this.handle_event(constants.EVENT_ZOOM_CHANGE, this.scale_x)
    }

    ////////////////////////////////////////////////////////////////////////////
    // INTERACTION

    _handle_spell_selected(selected_spells) {
        this.has_selection = selected_spells.length > 0;
    }

    _handle_check_images_loaded() {
        // Emit a EVENT_IMAGES_LOADED event once all images have been loaded.
        // until then, periodically emit new "check"-events
        const has_pending = this.rows.some(row => row.foreground.casts.some(cast => cast.image_is_loaded == false))
        if (has_pending) {
            setTimeout(() => { this.handle_event(constants.EVENT_CHECK_IMAGES_LOADED) }, 200)
            return
        }
        this.handle_event(constants.EVENT_IMAGES_LOADED)
    }

    handle_event(event_name, payload) {

        if (event_name === constants.EVENT_SPELL_SELECTED ) { this._handle_spell_selected(payload)}
        if (event_name === constants.EVENT_CHECK_IMAGES_LOADED ) { return this._handle_check_images_loaded() } // return here, as this event should not be passed on

        // pass to children
        this.ruler.handle_event(event_name, payload)
        this.rows.forEach(row => row.handle_event(event_name, payload))

        this.batchDraw() // for now, just assume we need to redraw after every event
    }

    ////////////////////////////////////////////////////////////////////////////
    // LOAD
    //

    set_spells(spells) {
        // create Spell Instances
        Object.values(spells).forEach(spell => {
            this.spells[spell.spell_id] = new Spell(this, spell);
        })
    }

    add_row(fight, player) {

        if (!(player && player.name)) { return}

        const row = new PlayerRow(fight, player)
        this.rows.push(row)

        this.back_layer.add(row.background)
        this.main_layer.add(row.foreground)

        // todo: don't do this in here
        this.longest_fight = Math.max(this.longest_fight, row.duration)
    }

    set_fights(new_fights) {

        // clear any old rows
        this.rows.forEach(row => {
            row.destroy()
        })
        this.fights = []
        this.longest_fight = 0
        this.rows = []

        // create fresh instances
        new_fights.forEach((fight) => {

            this.add_row(fight, fight.boss)
            fight.players.forEach(player => this.add_row(fight, player))
        })

        this.layout_children()

        this.ruler.update_duration(this.longest_fight)
        this.update_width()

        this.handle_event(constants.EVENT_ZOOM_CHANGE, this.scale_x)
        this.handle_event(constants.EVENT_CHECK_IMAGES_LOADED)
    }
}
