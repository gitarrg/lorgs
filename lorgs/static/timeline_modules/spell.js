

class Spell {

    constructor(stage, spell_data) {

        this.stage = stage
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
            image: spell_data.button,
            // listening: false,
            x: 3.5, // padding
            y: 3.5, // padding
            width: 20,
            height: 20,
            cornerRadius: 3,

            stroke: "black",
            strokeWidth: 1,
            transformsEnabled: "position",
        })
        this.cast_icon.perfectDrawEnabled(false);

        // Build the Group
        // this.group = new Konva.Group();
        // this.group.visible(this.show)

        if (true || this.duration > 0) {
            this.cast_duration = new Konva.Rect({
                name: "cast_duration",
                width: this.duration * stage.scale_x,
                height: LINE_HEIGHT-1,
                fill: this.color,
                cornerRadius: 3,
                opacity: 0.5,
                listening: true,
                transformsEnabled: "none",
            })
            this.cast_duration.perfectDrawEnabled(false);
        }

        if (true || this.cooldown) {
            this.cast_cooldown = new Konva.Rect({
                name: "cast_cooldown",
                width: this.cooldown * stage.scale_x,
                height: LINE_HEIGHT-1,
                fill: this.color,
                cornerRadius: 3,
                opacity: 0.1,
                listening: false,
                transformsEnabled: "none",
            })
            this.cast_cooldown.perfectDrawEnabled(false);
        }
    }

    load_icon () {
        // not used anymore..
        // we just get the icon from the button now

        let icon = this.cast_icon
        let prom = new Promise(resolve => {

            var image = new Image();
            image.onload = function() {
                icon.image(image)
                // icon.cache()
                resolve()
            }
            // image.crossOrigin = 'Anonymous'; // fix CORS
            // image.src = "/static/images/spells/" + this.data.icon
            if (this.data.icon.startsWith("/")) {
                image.src = this.data.icon;
            } else {
                image.src = "https://wow.zamimg.com/images/wow/icons/medium/" + this.data.icon
            }
        })
        // this.icon_img.src = "https://wow.zamimg.com/images/wow/icons/medium/" + this.data.icon
        return prom
    }
}
