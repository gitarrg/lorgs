

class Stage extends Konva.Stage{

    ZOOM_RATE = 1.1
    ZOOM_MIN = 0.5

    // global display options
    display_cooldown = true
    display_duration = true
    display_casttime = true

    constructor(options) {
        options.draggable = true
        super(options);
        this.transformsEnabled("position");

        // this.spec_slug = "";
        // this.boss_slug = "";

        this.scale_x = 4;
        this.fights = []
        this.spells = []

        STAGE = this;
        Cast.prototype.stage = this;

        // bool: true if any spell is selected
        this.has_selection = false;

        // bool: used to indicate if objects need to be rescaled
        this.zoom_changed = true; // true for initial load

        // create layers
        this.back_layer = new Konva.Layer({listening: false})
        this.add(this.back_layer);

        this.main_layer = new Konva.Layer()
        this.add(this.main_layer);

        this.overlay_layer = new Konva.Layer()
        this.add(this.overlay_layer);

        this.debug_layer = new Konva.Layer()
        this.add(this.debug_layer);

        // this.players = []
        this.ruler = new TimelineRuler(this);

        this.back_layer.add(this.ruler)

        this.longest_fight = 0;

        this.on("dragmove",  this.on_dragmove)
        this.on("wheel",  this.on_wheel)


        this.on('contextmenu', (e) => {
            e.evt.preventDefault();
        });

        // this.on("mousedown", (e) => {
        //     console.log("clicked stage")
        // })

    }

    ////////////////////////////////////////////////////////////////////////////
    // CREATION AND DRAW
    //
    create_ctx_menu() {

    }

    create() {

        this.main_layer.clear()
        let y = 0;

        y += (this.ruler.height-1)

        // update longest_fight
        this.longest_fight = 0;
        this.fights.forEach((fight, i) => {

            fight.create();  // <-- slow

            // background
            fight.y(y) // - 0.5)
            this.main_layer.add(fight)

            fight.background.y(y) // - 0.5)
            this.back_layer.add(fight.background)

            this.longest_fight = Math.max(this.longest_fight, fight.duration)
            y += LINE_HEIGHT
        })

        // Ruler
        console.time("ruler create")
        this.ruler.duration = this.longest_fight || 5 * 60;
        this.ruler.create();
        console.timeEnd("ruler create")

        // this.create_debug_layer()
        // var marker = new TimelineMarker();
        // this.debug_layer.add(marker)
    }

    update() {

        Konva.autoDrawEnabled = false;

        // ruler
        this.ruler.update()

        // fights
        this.fights.forEach((fight, i) => {
            fight.update();
        });

        Konva.autoDrawEnabled = true;
        this.main_layer.batchDraw();

        this.zoom_changed = false;

        // this.main_layer.cache()

    }

    ////////////////////////////////////////////////////////////////////////////
    // EVENTS
    //

    _limit_movement() {
        this.y(0);
        this.x(Math.min(this.x(), 0))
    }

    on_dragmove() {
        this._limit_movement()
    }

    on_wheel(event) {
        event.evt.preventDefault();

        let pointer = this.getPointerPosition();

        let old_offset = ( pointer.x - this.x()) / this.scale_x; // normalized distance between 0:00 and cursor

        this.scale_x = event.evt.deltaY < 0 ? this.scale_x * this.ZOOM_RATE : this.scale_x / this.ZOOM_RATE;
        this.scale_x = Math.max(this.scale_x, this.ZOOM_MIN)
        this.zoom_changed = true

        let new_offset = (old_offset * this.scale_x); // distance between 0:00 and cursor (new scale)
        let new_x = pointer.x - new_offset;

        this.x(new_x);
        this._limit_movement()

        // update_debug_layer()
        this.update();
    }

    ////////////////////////////////////////////////////////////////////////////
    // INTERACTION

    show_spell(spell_id, show=true) {

        let spell = this.spells[spell_id]
        if (!spell) {
            return
        }
        spell.show = show;
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

    // async load_spell_icons() {
    //     //////////////////////////
    //     // Load Images
    //     var promisses = [];
    //     this.spells.forEach(spell => {
    //         promisses.push(spell.load_icon())
    //     })
    //     await Promise.all(promisses); // wait for all the images to be loaded
    // }

    set_spells(spells_data) {

        // create Spell Instances
        spells_data.forEach(spell_data => {
            this.spells[spell_data.spell_id] = new Spell(this, spell_data);
        })
    }

    set_players(players) {

        players.forEach((player) => {
            let fight = new Fight(player.fight);
            fight.load_actors([player])
            this.fights.push(fight)
        })
    }


    ////////////////////////////////////////////////////////////////////////////
    // DEBUGGIN
    //

    print_tree() {
        // Debug
        let n = 0;
        var children = []
        this.find(node => {
            const d = node.getDepth()
            console.log("node", "\t".repeat(d), node.getType(), node.name(), node.visible())
            n+=1;
        })
        console.log("num stage objects:", n)
    }


}

