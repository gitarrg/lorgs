// TODO: reimplement

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

