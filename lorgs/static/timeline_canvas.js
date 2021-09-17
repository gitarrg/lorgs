


////////////////////////////////////////////////////////////////////////////////
// CONSTANTS

const LINE_HEIGHT = 28;


const CAST_DURATION_OPACITY_DEFAULT = 0.5
const CAST_DURATION_OPACITY_HOVER = 0.75
const CAST_DURATION_OPACITY_SELECTED = 0.8


const MODE_DEFAULT = 0
const MODE_HOVER = 1
const MODE_SELECTED = 2

var STAGE;


////////////////////////////////////////////////////////////////////////////////
// Scene Elements
//

class TimelineRuler extends Konva.Group {

    tick_distance = 10; // seconds
    timestamp_distance = 30;
    color = "white";
    height = LINE_HEIGHT;

    constructor(config) {
        super(config)
        this.listening(false)

        this.duration = 0; // time in seconds

        this.ticks = [];
        this.timestamps = [];

        // const tick_sm = new Konva.Line({
        //     name: "ruler_tick",
        //     points: [0, 0, 0, height],
        //     stroke: "red",
        //     strokeWidth: 3,
        // })

    }

    create() {

        // reset
        this.ticks = [];
        this.timestamps = [];

        for (var t=0; t<this.duration; t+=this.tick_distance) {

            let big = (t % this.timestamp_distance) == 0;
            let h = big ? 10 : 5

            const tick = new Konva.Line({
                name: "tick",
                points: [0.5, this.height-h, 0.5, this.height-1],
                stroke: this.color,
                strokeWidth: 1,
            })
            tick._time = t;


            this.ticks.push(tick)
            this.add(tick)

            if (big) {

                let text = new Konva.Text({
                    text: toMMSS(t),
                    name: "timestamp",
                    // x: 27,
                    y: -10,
                    fontSize: 14,
                    height: LINE_HEIGHT,
                    verticalAlign: 'bottom',
                    align: "center",
                    fontFamily: "Lato",
                    fill: this.color,
                    // listening: false,
                })
            this.timestamps.push(text)
            this.add(text)
            }
        }
    }

    update() {
        this.find(".tick").forEach((tick, i) => {
            tick.x(this.tick_distance * i * SCENE.scale_x);
        })

        this.find(".timestamp").forEach((timestamp, i) => {
            let x = this.timestamp_distance * i * SCENE.scale_x
            x += i==0 ? 0 : -18;
            timestamp.x(x)
        })
        this.cache()
    }

}



////////////////////////////////////////////////////////////////////////////////
// Timeline Elements
//

class Spell {

    constructor(spell_data) {

        this.data = spell_data

        // alias those attributes for easier access
        this.spell_id = this.data.spell_id;
        this.cooldown = this.data.cooldown || 0;
        this.duration = this.data.duration || 0;
        this.color = this.data.color;
        this.show = this.data.show;

        this.selected = false;

        this.cast_icon = new Konva.Image({
            name: "icon",
            // image: this.icon,
            // listening: false,
            x: 3.5, // padding
            y: 3.5, // padding
            width: 20,
            height: 20,
            cornerRadius: 3,

            stroke: "black",
            strokeWidth: 1,
        })


        // Build the Group
        // this.group = new Konva.Group();
        // this.group.visible(this.show)

        this.cast_duration = new Konva.Rect({
            name: "duration",
            width: this.duration * SCENE.scale_x,
            height: LINE_HEIGHT,
            fill: this.color,
            cornerRadius: 3,
            opacity: 0.5,
            visible: this.duration > 0,
        })

        this.cast_cooldown = new Konva.Rect({
            name: "cooldown",
            width: this.cooldown * SCENE.scale_x,
            height: LINE_HEIGHT,
            fill: this.color,
            cornerRadius: 3,
            opacity: 0.1,
            listening: false,
            visible: this.cooldown > 0,
        })

        this.cast_icon.perfectDrawEnabled(false);
        this.cast_duration.perfectDrawEnabled(false);
        this.cast_cooldown.perfectDrawEnabled(false);

        // this.cooldown.opacity = 0.1
        // this.cooldown.rx = 3;
        // this.cooldown.ry = 3;
        // this.cooldown.fill = this.spell.color
        // this.cooldown.width = SCENE.scale_x * this.spell.cooldown
        // this.cooldown.height = LINE_HEIGHT
        // this.group.addWithUpdate(this.cooldown);
        // this.group.add(this.cast_cooldown);
    }

    load_icon () {

        let icon = this.cast_icon

        let prom = new Promise(resolve => {

            var image = new Image();
            image.onload = function() {
                icon.image(image)
                icon.cache()
                resolve()
            }
            // image.crossOrigin = 'Anonymous'; // fix CORS
            // image.src = "/static/images/spells/" + this.data.icon
            image.src = "https://wow.zamimg.com/images/wow/icons/medium/" + this.data.icon
        })
        // this.icon_img.src = "https://wow.zamimg.com/images/wow/icons/medium/" + this.data.icon
        return prom
    }
}


class Cast extends Konva.Group {


    constructor(cast_data, config) {
        super(config)

        this.mode = MODE_DEFAULT
        this.stage = this.getStage() || STAGE;

        this.hovering = false

        // Spell Info
        this.spell_id = cast_data.spell_id;
        this.spell = this.stage.spells[this.spell_id];
        this.timestamp = cast_data.timestamp / 1000;
        // this.listening(true);

        // Cast Info
        if (this.spell === undefined) {
            // console.log(`spell ${this.spell_id} not found.`)
            this.visible(false)
            return
        }
        this.visible(this.spell.show)


        this.cast_cooldown = this.spell.cast_cooldown.clone()
        this.add(this.cast_cooldown);

        this.cast_duration = this.spell.cast_duration.clone()
        this.add(this.cast_duration);

        this.cast_icon = this.spell.cast_icon.clone()

        // this.cast_icon.filters([Konva.Filters.Grayscale]);
        this.add(this.cast_icon);

        // this.cache()
        // this.filters([Konva.Filters.Blur])

        // this.spell_group = this.spell.group.clone()
        // this.add(this.spell_group);

        // this.cache()
        // this.group.cache();

        // this.on('mouseover', (event) => {
        //     console.log("hello!")
        // });
        this.on('mousedown', this.select);
        this.on('mouseover', () => {this.hover(true)});
        this.on('mouseout', () => {this.hover(false)});
    }

    create() {

        this.cast_text = new Konva.Text({
            text: toMMSS(this.timestamp),
            x: 27,
            y: 0,
            fontSize: 14,

            height: LINE_HEIGHT,
            verticalAlign: 'middle',

            fontFamily: "Lato",
            fill: "white",
            listening: true,
            }
        )
        this.add(this.cast_text);
        // hover events
    }

    update() {

        // console.log("update scene")

        if (!this.spell) { return; }

        this.visible(this.spell.show)
        if (!this.visible) { return; }


        const stage = this.getStage()
        const scale_x = stage.scale_x;

        this.x(scale_x * this.timestamp)


        // default state
        this.cast_text.fontStyle("normal");
        this.cast_text.fill("white");
        this.cast_duration.opacity(0.5)
        this.cast_cooldown.opacity(0.1)

        this.cast_icon.opacity(1.0)
        // this.cast_icon.saturation(0)
        this.cast_icon.strokeWidth(1)

        this.opacity(1.0)
        // this.blurRadius(0)

        if (stage.has_selection) {
            if (this.spell.selected) {
                // this.moveToTop()
                // this.cast_text.fill("lime")
                this.cast_text.fontStyle("bold");
                this.cast_duration.opacity(0.85)
                this.cast_cooldown.opacity(0.4)
            } else {
                this.opacity(.5)
                this.cast_text.fill("#ccc")
                this.cast_icon.opacity(0.5)

                // this.cast_icon.saturation(-10)
                this.cast_icon.strokeWidth(0)
                // this.blurRadius(2)
            }
        }
        else if (this.hovering) {
            // this.cast_text.fill("yellow")
            this.cast_text.fontStyle("normal");
            this.cast_duration.opacity(0.75)
            this.cast_cooldown.opacity(0.3)
        }

        /*
        this.mode = (stage.has_selection && this.spell.selected) ? MODE_SELECTED : this.mode
        switch(this.mode) {

            case MODE_SELECTED:
            break

            case MODE_HOVER:
            break

            case MODE_DEFAULT:
            default:
                this.cast_text.fill("white")
                this.cast_text.fontStyle("normal");
                this.cast_duration.opacity(0.5)
        }

        if (stage.has_selection) {

            // style: selected spell
            if (this.spell.selected) {
                this.cast_text.fill("lime")
                this.cast_duration.opacity(CAST_DURATION_OPACITY_SELECTED)

            // style: un-selected spell
            } else {
                this.cast_text.fontStyle("italic");
                this.cast_duration.opacity(CAST_DURATION_OPACITY_DEFAULT)
            }
            return
        }
        */

        this.cast_duration.width(this.spell.duration * scale_x)
        this.cast_cooldown.width(this.spell.cooldown * scale_x)
        // this.spell_group.find(".duration").forEach(duration => {
        // })
        // this.spell_group.find(".cooldown").forEach(cooldown => {
        // })
        // this.spell_group.cache();
        // this.cache();
    }

    hover(state) {

        this.hovering = state;

        this.update()

        const stage = this.getStage()
        stage.container().style.cursor = this.hovering ? "pointer" : "grab";

        // make sure to fall back to the selected state if applicable
        // this.mode = this.spell.selected ? MODE_SELECTED : MODE_DEFAULT;
        // this.mode = state ? MODE_HOVER : this.mode

        // this.spell_group.find(".cooldown").forEach(cooldown => {
        //     cooldown.opacity(state ? 0.3 : 0.1);
        // })
    }

    select() {

        const stage = this.getStage()

        stage.has_selection = false
        stage.spells.forEach(spell => {
            spell.selected = (spell == this.spell) && !this.spell.selected

            // if (spell == this.spell) {
            //     spell.selected = !spell.selected;
            //     console.log("new state", this.spell.selected)
            // } else {
            //     spell.selected = false;
            // }
            stage.has_selection = stage.has_selection || spell.selected;
        })

        // this.spell.selected = !this.spell.selected

        this.spell.selected = this.spell.selected || stage.has_selection
        this.mode = this.spell.selected ? MODE_SELECTED : MODE_DEFAULT

        stage.update()
    }

}


class Player {

    constructor(player_data) {

        this.name = player_data.name
        this.y = 0;  // offset in y

        this.total_fmt = "10k";
        this.casts_group = new Konva.Group()

        // load casts
        this.casts = [];
        player_data.casts.forEach(cast_data => {
            this.casts.push(new Cast(cast_data))
        })

        /*
        this.group = new fabric.Group();
        this.group.selectable = false;

        this.background = new fabric.Rect({
            left: 0,
            top: 0,
            fill: "hsl(0, 0%, 30%)",
            width: 175,
            height: LINE_HEIGHT
        });
        this.text_name = new fabric.Text(
            this.name,
            {
                left: 0,
                top: 0,
                fontSize: 19,
                textAlign: 'center',
                fontFamily: "Lato",
                fill: "white",
            }
        );
        this.group.addWithUpdate(this.background);
        this.group.addWithUpdate(this.text_name);
        // this.name
        */
    }

    create() {
        this.casts.forEach(cast => {
            cast.create()
            this.casts_group.add(cast)
        })
    }

    update() {
        this.casts.forEach(cast => {
            cast.update()
        })
    }
}


class Fight extends Konva.Group {

    constructor(fight_data) {
        super()
        // this.listening(false)

        this.duration = fight_data.duration / 1000; // ms to s
        this.duration = Math.ceil(this.duration);


        this.players = [];

        let boss = fight_data.boss
        if (boss && boss.casts) {
            this.players.push(new Player(boss))
        }

        fight_data.players.forEach(player_data => {
            this.players.push(new Player(player_data))
        })

        const y = LINE_HEIGHT * this.players.length;

        this.clip({
            x: 0,
            y: -1,
            width: 200,
            height: y+1,
        })

        this.background = new Konva.Rect({
            height: y,
            // width: 20,
            x: -1.5,
            y: -0.5,
            fill: "#222",
            stroke: "black",
            strokeWidth: 1,
        })
        this.add(this.background)
    }

    create() {

        this.players.forEach((player, i) => {
            player.create();
            this.add(player.casts_group);
            player.casts_group.y(i * LINE_HEIGHT)

        })
    }

    update() {
        const w = this.duration * SCENE.scale_x;

        this.background.width(w)
        this.clipWidth(w+1)

        this.players.forEach(player => {
            player.update();
        })
    }
}


class Scene extends Konva.Stage{

    ZOOM_RATE = 1.1;

    constructor(options) {
        super(options);

        this.spec_slug = "";
        this.boss_slug = "";

        STAGE = this;

        // bool: true if any spell is selected
        this.has_selection = false;

        this.scale_x = 4;
        this.fights = []
        this.spells = []

        // this.players = []
        this.ruler = new TimelineRuler();
        this.longest_fight = 0;

        this.on("dragmove",  this.on_dragmove)
        this.on("wheel",  this.on_wheel)

        this.main_layer = new Konva.Layer()
        this.add(this.main_layer);

    }

    create(ctx) {

        this.main_layer.clear()
        let y = 0;

        y += this.ruler.height

        // update longest_fight
        this.longest_fight = 0;
        this.fights.forEach((fight, i) => {


            fight.create();
            fight.y(y) // his.ruler.height + i*(LINE_HEIGHT))
            this.main_layer.add(fight)

            y += fight.background.height()
            console.log("y", y)

            this.longest_fight = Math.max(this.longest_fight, fight.duration)


        })
        this.ruler.duration = this.longest_fight;
        this.ruler.create();
        this.main_layer.add(this.ruler)

        // this.height


    }

    update() {

        this.ruler.update()

        this.fights.forEach((fight, i) => {
            fight.update();
        });

    }

    ///////////////////////////////////

    _limit_movement() {
        this.y(0);
        this.x(Math.min(this.x(), 0))
    }

    on_dragmove() {
        this._limit_movement()
    }

    on_wheel(event) {
        event.evt.preventDefault();

        // var oldScale = stage.scaleX();
        // var pointer = stage.getPointerPosition();
        // var mousePointTo = {
        //     x: (pointer.x - stage.x()) / oldScale,
        //     y: (pointer.y - stage.y()) / oldScale,
        // };

        let pointer = this.getPointerPosition();

        let old_offset = ( pointer.x - this.x()) / SCENE.scale_x; // normalized distance between 0:00 and cursor
        // const old_x = (stage.x()+pointer.x) / SCENE.scale_x;

        SCENE.scale_x = event.evt.deltaY < 0 ? SCENE.scale_x * this.ZOOM_RATE : SCENE.scale_x / this.ZOOM_RATE;


        let new_offset = (old_offset * SCENE.scale_x); // distance between 0:00 and cursor (new scale)
        let new_x = pointer.x - new_offset;

        // console.log("e.evt.deltaY", SCENE.scale_x)
        // const new_x = old_x * SCENE.scale_x;
        // console.log("old x", old_x, "new_x", new_x);

        this.x(new_x);
        this._limit_movement()

        // update_debug_layer()
        this.update();


        // stage.scale({ x: newScale, y: 1 });
        // var newPos = {
        //     x: pointer.x - mousePointTo.x * newScale,
        //     y: 0,
        // };
        // stage.position(newPos);
    }

    ////////////////////////////////////////////////////////////////////////////
    //

    show_spell(spell_id, show=true) {

        let spell = this.spells[spell_id]
        if (!spell) {
            return
        }
        spell.show = show;
        this.update();
    }

    ////////////////////////////////////////////////////////////////////////////
    //

    show_loading() {

        let text = new Konva.Text({
            text: "loading....",
            x: 50,
            y: 50,
            fontSize: 36,
            height: LINE_HEIGHT,
            verticalAlign: 'bottom',
            align: "left",
            fontFamily: "Lato",
            fill: "white",
            listening: false,
        })

        this.main_layer.add(text)
    }

    async load_spell_icons() {
        //////////////////////////
        // Load Images
        var promisses = [];
        this.spells.forEach(spell => {
            promisses.push(spell.load_icon())
        })
        await Promise.all(promisses); // wait for all the images to be loaded
    }

    async load_spells(spec_slug) {

        let params = new URLSearchParams({"group": spec_slug})
        let url ="/api/spells?" + params
        let response = await fetch(url);

        if (response.status != 200) {
            return
        }
        let data = await response.json();

        // create Spell Instances
        for(var i in data) {
            var spell_data = data[i];
            var spell = new Spell(spell_data);
            this.spells[spell_data.spell_id] = spell;
        }

    }

    async load_fights(spec_slug, boss_slug) {

        let url = `/api/spec_ranking/${spec_slug}/${boss_slug}`
        let response = await fetch(url);
        if (response.status != 200) {
            return
        }

        let data = await response.json();

        // update scene
        this.fights = [];

        data.fights.forEach((fight_data, i) => {
            let fight = new Fight(fight_data);
            this.fights.push(fight);
        })
    }

    async load(spec_slug, boss_slug) {

        this.show_loading()

        await this.load_spells(SPEC_SLUG);
        await this.load_spell_icons();
        await this.load_fights(SPEC_SLUG, BOSS_SLUG);
        this.create()
        this.update();
    }


}







