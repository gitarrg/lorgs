

import Konva from "konva"

import Fight from "./Fight.js"
import Player from "./Player.js"
import Ruler from "./Ruler.js"
import Spell from "./Spell.js"
import {LINE_HEIGHT} from "./../../constants.js"


// for performance
Konva.autoDrawEnabled = false;


export default class Stage extends Konva.Stage{

    ZOOM_RATE = 1.1
    ZOOM_MIN = 0.5

    FIGHT_SPACE = 10 // distance between fights in pixels

    // global display options
    display_cooldown = true
    display_duration = true
    display_casttime = true
    display_casticon = true

    constructor(options) {
        options.draggable = true
        options.strokeScaleEnabled = false
        super(options);

        /////////////////////////////////
        // custom attributes
        this.scale_x = 4;
        this.fights = []
        this.spells = {}
        this.longest_fight = 0;

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
        // window.addEventListener("resize", () => {this.update_size()})
        this.on("dragmove",  this.on_dragmove)
        this.on("wheel",  this.on_wheel)
        this.on("contextmenu", this.contextmenu)

        document.addEventListener("toggle_spell", event => { this.show_spell(event.spell_id, event.show) })
    }

    ////////////////////////////////////////////////////////////////////////////
    // CREATION AND DRAW
    //
    contextmenu(event) {
        event.evt.preventDefault();
    }

    create() {

        this.clear()
        this.zoom_changed = true
        this.longest_fight = 0;

        // update fights
        this.fights.forEach((fight, i) => {

            // create/add the fight
            // fight.y(this.ruler.height-1 + (i*LINE_HEIGHT))
            this.main_layer.add(fight)
            // this.back_layer.add(fight.background)
            fight.create();

            // background need to be added separately
            fight.actors.forEach(actor => {this.back_layer.add(actor.background)})

            // get longest fight (for the ruler)
            this.longest_fight = Math.max(this.longest_fight, fight.duration)
        })

        // Ruler
        this.ruler.duration = this.longest_fight || 5 * 60;
        this.ruler.create();

        // update height based on number of fights loaded
        // this.height(this.ruler.height + this.fights.length * LINE_HEIGHT)
    }

    update() {

        // ruler
        this.ruler.update()

        // fights
        let y = this.ruler.height-1;
        this.fights.forEach((fight, i) => {
            fight.update();

            if (fight.visible()) {
                fight.y(y)
                // fight.background.y(y)
                // fight.cache()
                y += fight.height() + this.FIGHT_SPACE
            }
        });

        this.height(y)
        this.batchDraw();
        this.zoom_changed = false;
    }

    schedule_update() {

        if (this.timer) { return }
        
        this.timer = setTimeout(() => {
            this.update()
            delete this.timer
        }, 300)
    }

    update_has_selection() {
        let spells = Object.values(this.spells)
        this.has_selection = spells.some(spell => (spell.selected && spell.show))
    }

  
    ////////////////////////////////////////////////////////////////////////////
    // EVENTS
    //
    
    update_size() {
        // TODO: get parent width (after overflow etc)
        this.width(this.longest_fight * this.scale_x)
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
        this.zoom_changed = true

        let new_offset = (old_offset * this.scale_x); // distance between 0:00 and cursor (new scale)
        let new_x = pointer.x - new_offset;

        this.x(new_x);
        this._limit_movement()

        ////////////////////////////////////
        // update scale

        this.update();
    }

    ////////////////////////////////////////////////////////////////////////////
    // INTERACTION

    show_spell(spell_id, show=true, update=true) {

        let spell = this.spells[spell_id]
        if (!spell) {
            return
        }
        spell.show = show;
        if (!update) {return}

        this.update_has_selection()
        this.update();
    }

    toggle_cooldown(show=true) {
        this.display_cooldown = show;
        this.update()
    }

    toggle_duration(show=true) {
        this.display_duration = show;
        this.update()
    }

    toggle_casttime(show=true) {
        this.display_casttime = show;
        this.update()
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

    set_fights(new_fights) {

        // clear any old fights
        this.fights.forEach(fight => {
            fight.destroy()
            // fight.background.destroy()
        })
        this.fights = []

        // create fresh instances
        new_fights.forEach((fight) => {

            const new_fight = new Fight(this, fight);
            this.fights.push(new_fight)
        })


/*             let boss = fight.boss
            if (boss && boss.name) {
                let new_fight = new Fight(this, fight);
                new_fight.actors.push(new Player(this, boss))
                this.fights.push(new_fight)
            }
            
            let new_fight = new Fight(this, fight);
            fight.players.forEach(player => {
                new_fight.actors.push(new Player(this, player))
                this.fights.push(new_fight)
            }) */
        // })
    }

    ////////////////////////////////////////////////////////////////////////////
    // DEBUGGIN
    //

    print_tree() {
        // Debug
        let n = 0;
        this.find(node => {
            const d = node.getDepth()
            console.log("node", "\t".repeat(d), node.getType(), node.name(), node.visible())
            n+=1;
        })
        console.log("num stage objects:", n)
    }
}

