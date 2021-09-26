

import {LINE_HEIGHT} from "./vars.js"


class CastTooltip extends Konva.Group {

    PADDING = 8

    constructor(cast, options) {
        super(options)
        this.listening(false)
        this.transformsEnabled("position")

        let label = `${cast.spell.name}`
        if (cast.count) {
            label += ` #${cast.count}`
        }
        label += `\n`

        label += `${toMMSS(cast.timestamp)}`

        if (cast.spell.duration > 0) {
            label += ` - ${toMMSS(cast.timestamp+cast.spell.duration)}`
        }

        // Timestamp
        this.text = new Konva.Text({
            name: "tooltip_Text",
            text: label,
            // x: this.PADDING,
            // y: this.PADDING,
            fontSize: 14,

            verticalAlign: "bottom",

            fontFamily: "Lato",
            fill: "white",
            listening: false,
            transformsEnabled: "position",
            }
        )

        const box = new Konva.Rect({
            x: this.text.x(),
            y: this.text.y(),
            width: this.text.width() + 2 * this.PADDING,
            height: this.text.height() + 2 * this.PADDING,

            fill: "black",
            opacity: 1,
            cornerRadius: 4,
        });

        this.text.move({x: this.PADDING, y: this.PADDING})

        this.add(box);
        this.add(this.text)
    }
}


export default class Cast extends Konva.Group {

    constructor(stage, cast_data, config) {
        super(config)

        // Kova Attrs
        this.listening(true)
        this.transformsEnabled("position")
        this.name("Cast")
        this.stage = stage

        // Spell Info
        this.spell_id = cast_data.id;
        this.timestamp = cast_data.ts / 1000;
        this.count = cast_data.count;
        this.spell = this.stage.spells[this.spell_id];

        // Internal Attrs
        this.hovering = false
        this.tooltip;
        this.tooltip_timer;


    }

    create() {

        // this.spell = this.stage.spells[this.spell_id];
        if (this.spell === undefined) {
            this.remove()  // yeet!
            return
        }


        this.visible(this.spell.show)

        // Setup Events
        this.on('mousedown', this.select);  // TODO: only on left click
        this.on('mouseover', () => {this.hover(true)});
        this.on('mouseout', () => {this.hover(false)});


        // Cast Cooldown
        this.cast_cooldown = this.spell.cast_cooldown.clone()
        if (this.spell.cooldown > 0) {
            this.add(this.cast_cooldown)
        }

        // Cast Duration
        this.cast_duration = this.spell.cast_duration.clone()
        if (this.spell.duration > 0) {
            this.add(this.cast_duration)
        }

        // Cast Icon
        this.cast_icon = this.spell.cast_icon.clone()
        this.add(this.cast_icon)

        // Timestamp
        this.cast_text = new Konva.Text({
            name: "cast_timestamp",
            text: toMMSS(this.timestamp),
            x: 27,
            y: 0,
            fontSize: 14,

            height: LINE_HEIGHT,
            verticalAlign: 'middle',

            fontFamily: "Lato",
            fill: "white",
            listening: false,
            transformsEnabled: "position",
            }
        )
        this.cast_text.perfectDrawEnabled(false);
        this.add(this.cast_text);

        // invisible box for mouse events
        // (some casts might not have a duration-bar to use)
        const bbox = new Konva.Rect({
            width: this.cast_text.x() + this.cast_text.width() + 3,
            height: LINE_HEIGHT-1,
        });
        this.add(bbox)

        this.y(1);

    }

    update() {

        if (!this.spell) { return; }

        const update_vis = this.visible() != this.spell.show;

        this.visible(this.spell.show)
        if (!this.visible()) { return;}

        const stage = this.stage

        if (update_vis || stage.zoom_changed) {
            this.x(stage.scale_x * this.timestamp)
            this.cast_duration.width(this.spell.duration * stage.scale_x)
            this.cast_cooldown.width(this.spell.cooldown * stage.scale_x)
        }


        // update element visibility
        this.cast_text.visible(stage.display_casttime)
        this.cast_cooldown.visible(stage.display_cooldown)
        this.cast_duration.visible(stage.display_duration)
        this.cast_icon.visible(stage.display_casticon)

        // default state
        this.cast_text.fontStyle("normal");
        this.cast_text.fill("white");
        this.cast_duration.opacity(0.5)
        this.cast_cooldown.opacity(0.1)
        this.cast_icon.opacity(1.0)
        this.cast_icon.strokeWidth(1)
        this.opacity(1.0)

        if (stage.has_selection) {
            if (this.spell.selected) {
                this.cast_text.fontStyle("bold");
                this.cast_duration.opacity(0.85)
                this.cast_cooldown.opacity(0.4)
            } else {
                this.opacity(.5)
                this.cast_text.fill("#ccc")
                this.cast_icon.opacity(0.5)
                this.cast_icon.strokeWidth(0)
            }
        }
        else if (this.hovering) {
            this.cast_duration.opacity(0.75)
            this.cast_cooldown.opacity(0.3)
        }
    }

    hover(state) {

        this.hovering = state;
        this.update()

        // update group
        const casts_group = this.getParent();
        casts_group.cache()  // refresh cache for this group

        // update layer
        let layer = this.getLayer()
        layer.batchDraw()

        // update cursor
        const stage = this.getStage()
        stage.container().style.cursor = this.hovering ? "pointer" : "grab";


        // Hacky Tooltip logic FIXME
        if (this.hovering) {

            if (this.tooltip_timer === undefined) {
                this.tooltip_timer = setTimeout(() => {
                    this.tooltip = new CastTooltip(this)
                    this.stage.overlay_layer.add(this.tooltip)
                    this.tooltip.absolutePosition(this.absolutePosition())
                    this.tooltip.move({x: 40, y: -30})
                    this.stage.overlay_layer.batchDraw()
                }, 500)
            }
        } else {

            if (this.tooltip_timer) {
                clearTimeout(this.tooltip_timer)
                this.tooltip_timer = undefined
            }

            if (this.tooltip) {
                this.tooltip.hide()
                this.tooltip.remove()
                this.tooltip = undefined
            }
        }
    }

    select(event) {

        if (event.evt.ctrlKey) {
            // keep current selection.. simply toggle the current spell
            this.spell.selected = !this.spell.selected

        } else {
            // regular selection:
            //  - deselect all spells
            //  - toogle the current spell
            let spells = Object.values(this.stage.spells)
            spells.forEach(spell => {
                spell.selected = (spell == this.spell) && !this.spell.selected
            })
        }
        this.stage.update_has_selection()
        this.stage.update()
    }
}
