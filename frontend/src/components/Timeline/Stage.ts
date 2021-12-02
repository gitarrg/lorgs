import Konva from "konva"
import type { StageConfig } from "konva/lib/Stage";

import Ruler from "./Ruler"
import * as constants from "./constants";
import FightRow from "./FightRow";
import type Fight from "../../types/fight";
import { IMAGES } from "./Cast";
import { MODES } from "../../store/ui";


// for performance
Konva.autoDrawEnabled = false;


export default class Stage extends Konva.Stage{

    static ZOOM_RATE = 1.1
    static ZOOM_MIN = 0.5

    static THROTTLE = 200 // max update rate in ms

    MODE = ""

    scale_x: number
    private rows: FightRow[] = []

    // bool: true if any spell is selected
    has_selection: boolean

    back_layer: Konva.Layer
    main_layer: Konva.Layer
    overlay_layer: Konva.Layer
    ruler: Ruler

    /** Duration of the longest fight. Used to set things such as the the Length of the Ruler and overall width. */
    longest_fight = 0


    constructor(options: StageConfig) {
        super(options);
        this.draggable(true)

        /////////////////////////////////
        // custom attributes
        this.scale_x = constants.DEFAULT_ZOOM

        this.rows = []

        // bool: true if any spell is selected
        this.has_selection = false;

        ////////////////////////////////
        // create layers
        this.back_layer = new Konva.Layer({listening: false})
        this.add(this.back_layer);

        this.main_layer = new Konva.Layer()
        this.add(this.main_layer);

        this.overlay_layer = new Konva.Layer()
        this.add(this.overlay_layer);

        this.ruler = new Ruler(this);
        this.back_layer.add(this.ruler)

        // update canvas on window resize
        this.on("dragmove",  this.on_dragmove)
        this.on("wheel",  this.on_wheel)
        this.on("contextmenu", this.contextmenu)

        // update canvas on window resize
        window.addEventListener("resize", () => {this.update_width()})
        this.update_width() // initial update
    }

    get FIGHT_SPACE() {
        // distance between fights in pixels
        if (this.MODE == MODES.SPEC_RANKING ) { return -1; }
        if (this.MODE == MODES.COMP_RANKING ) { return 10; }
        if (this.MODE == MODES.USER_REPORT ) { return 38; } // 1 row + 10px gap

        return -1;
    }

    ////////////////////////////////////////////////////////////////////////////
    // CREATION AND DRAW
    //
    update_width() {
        let container = this.container()
        this.width(container.offsetWidth)
    }

    layout_children() {

        let y = this.ruler.height()

        this.rows.forEach(row => {
            row.y(y)

            const row_height = row.height()
            if (row_height > 0) {
                y += row.height() + this.FIGHT_SPACE + 1 // 1px for border
            }
        })
        this.height(y+1) // 1 extra to show the border
    }

    ////////////////////////////////////////////////////////////////////////////
    // STANDARD EVENTS
    //

    contextmenu(event: Konva.KonvaEventObject<MouseEvent>) {
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

    on_wheel(event: Konva.KonvaEventObject<WheelEvent> ) {

        // only zoom on shift/ctrl + scroll
        if (! (event.evt.shiftKey || event.evt.ctrlKey)) { return;}
        event.evt.preventDefault();

        ////////////////////////////////////
        // update scale

        let pointer = this.getPointerPosition();
        if (!pointer) { return }

        let old_offset = ( pointer.x - this.x()) / this.scale_x; // normalized distance between 0:00 and cursor

        this.scale_x = event.evt.deltaY < 0 ? this.scale_x * Stage.ZOOM_RATE : this.scale_x / Stage.ZOOM_RATE;
        this.scale_x = Math.max(this.scale_x, Stage.ZOOM_MIN)

        let new_offset = (old_offset * this.scale_x); // distance between 0:00 and cursor (new scale)
        let new_x = pointer.x - new_offset;

        this.x(new_x);
        this._limit_movement()

        ////////////////////////////////////
        // update scale
        this.handle_event(constants.EVENT_ZOOM_CHANGE, this.scale_x)
    }

    ////////////////////////////////////////////////////////////////////////////
    // CUSTOM EVENTS

    _handle_spell_selected(selected_spells: number[]) {
        this.has_selection = selected_spells.length > 0;
    }

    _handle_check_images_loaded() {
        // Emit a EVENT_IMAGES_LOADED event once all images have been loaded.
        // until then, periodically emit new "check"-events
        const is_loading = Object.values(IMAGES).some(img => !img.complete)

        // try again later
        if (is_loading) {
            setTimeout(() => { this.handle_event(constants.EVENT_CHECK_IMAGES_LOADED) }, 200)
            return
        }
        // update now
        this.handle_event(constants.EVENT_IMAGES_LOADED)
    }

    _handle_apply_filters() {
        this.layout_children()
    }

    handle_event(event_name: string, payload?: any) {

        if (event_name === constants.EVENT_SPELL_SELECTED ) { this._handle_spell_selected(payload)}
        if (event_name === constants.EVENT_CHECK_IMAGES_LOADED ) { return this._handle_check_images_loaded() } // return here, as this event should not be passed on

        // pass to children
        this.ruler.handle_event(event_name, payload)
        this.rows.forEach(row => row.handle_event(event_name, payload))

        if (event_name === constants.EVENT_APPLY_FILTERS ) { this._handle_apply_filters()}

        this.batchDraw() // for now, just assume we need to redraw after every event
    }

    ////////////////////////////////////////////////////////////////////////////
    // LOAD
    //

    set_fights(new_fights: Fight[]) {

        // clear any old rows
        this.rows.forEach(row => {
            row.destroy()
        })

        this.longest_fight = 0
        this.rows = []

        // create fresh instances
        new_fights.forEach((fight) => {
            const row = new FightRow(fight)
            this.back_layer.add(row.background)
            this.main_layer.add(row.foreground)
            this.longest_fight = Math.max(this.longest_fight, row.duration)

            this.rows.push(row)
        })

        this.layout_children()

        this.ruler.update_duration(this.longest_fight)
        this.handle_event(constants.EVENT_ZOOM_CHANGE, this.scale_x)
        this.handle_event(constants.EVENT_CHECK_IMAGES_LOADED)
    }
}
