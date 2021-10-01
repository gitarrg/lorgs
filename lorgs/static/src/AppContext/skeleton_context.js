////////////////////////////////////////////////////////////////////////////////
// Random Context Generation (for the loading screen)
//

function create_random_casts() {

    let n_casts = randint(3, 10)
    let casts = []

    for(let c=0; c < n_casts; c++) {
        casts.push({
            "id": 0,
            "ts": randint(0, 240 * 1000)
        })
    }
    return casts
}

function create_random_player() {
    return {
        "name": "",
        "rank": -1,
        // "total": randint(250, 20000),
        "casts": create_random_casts(),
    }
}

function create_default_fights(n) {

    let fights = []

    for (let i = 0; i < n; i++) {
        let fight = {}
        fight.loading = true
        fight.duration = 1000 * randint(120, 240)
        fight.players = [create_random_player()]
        fight.report_id = `dummy_${i}`
        fights.push(fight)
    }
    return fights
}

export default function create_skeleton_context(context = {}) {

    context.spells = {}
    context.spells[0] = {"spell_id": 0, "color": "#ccc", "duration": 30, "show": true}

    context.fights = create_default_fights(15)
    return context
}
