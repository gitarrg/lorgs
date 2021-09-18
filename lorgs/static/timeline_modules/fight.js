

class Fight extends Konva.Group {

    constructor(fight_data) {
        super()
        this.name("Fight")
        this.listening(true)
        this.transformsEnabled("position")

        this.duration = fight_data.duration / 1000; // ms to s
        this.duration = Math.ceil(this.duration);

        this.actors = []
        this.clip({
            x: 0,
            y: 1,
            width: 200,
            height: LINE_HEIGHT,
        })


        this.background = new Konva.Group()
        this.background.name("fight_background")

        this.background_fill = new Konva.Rect({
            height: LINE_HEIGHT,
            // width: 20,
            x: -0.5,
            y: 0.5,
            fill: "#222",
            stroke: "black",
            strokeWidth: 1,
            listening: false,
            transformsEnabled: "position",
        })
        this.background.add(this.background_fill)
    }

    create() {
        this.actors.forEach((actor, i) => {
            actor.create();
            this.add(actor.casts_group);
            // actor.casts_group.y(i * LINE_HEIGHT)
        })
    }

    update() {
        const stage = this.getStage() || this.background.getStage();
        if (!stage) {return}

        let w = this.duration * stage.scale_x;
        w = Math.floor(w); // avoid drawing strokes on half pixels

        // update background
        this.background_fill.width(w)
        this.clipWidth(w-1) // clip content to show background stroke

        // update actors
        this.actors.forEach(actor => {actor.update()})
    }

    load_actors(actors_data) {
        actors_data.forEach(actor_data => {
            this.actors.push(new Player(actor_data))
        })
    }
}

