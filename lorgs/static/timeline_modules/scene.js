


import Stage from "./stage.js"


////////////////////////////////////////////////////////////////////////////////


async function load_spells(groups) {

    let params = new URLSearchParams(groups.map(g => ["group", g]))
    let url ="/api/spells?" + params

    let response = await fetch(url);
    if (response.status != 200) {
        return []
    }
    let data = await response.json()

    // convert into regular list
    // this is probl not needed.. but idk..
    let spells = []
    for(var i in data) {
        spells.push(data[i])
    }
    return spells;
}


async function load_fights(spec_slug, boss_slug) {

    let url = `/api/spec_ranking/${spec_slug}/${boss_slug}`;
    let response = await fetch(url);
    if (response.status != 200) {
        return;
    }
    let data = await response.json();
    return data.fights;
}


function spec_ranking_color(i=0) {

    if (i ==  1)  { return "text-artifact"   } else
    if (i <= 25)  { return "text-astounding" } else
    if (i <= 100) { return "text-legendary" }  else
                  { return "epic"}
}


function create_boss_name_div(boss) {

    let container = document.createElement("div")
    container.className = "boss_name"

    // fix zone name
    let class_icon = document.createElement("img");
    class_icon.className = "boss_name__spec_icon"
    class_icon.src = `/static/images/bosses/sanctum-of-domination/${boss.name_slug}.jpg`;
    container.appendChild(class_icon)

    let name = document.createElement("span");
    name.className = "boss_name__name"
    name.innerHTML = boss.name
    container.appendChild(name);

    return container
}


function create_player_name_div(player) {

    let container = document.createElement("div");
    container.className = "player_name " + spec_ranking_color(player.rank)

    let class_icon = document.createElement("img");
    class_icon.className = "player_name__spec_icon"
    class_icon.src = `/static/images/specs/${player.spec_slug}.jpg`;
    container.appendChild(class_icon)

    let wcl_link = document.createElement("a");
    wcl_link.target = "_blank"
    wcl_link.href = player.fight.report_url
    container.appendChild(wcl_link)

    let name = document.createElement("span");
    name.className = `player_name__name wow-class-${player.class_slug}`;
    name.innerHTML = player.name
    wcl_link.appendChild(name);

    let rank = document.createElement("span");
    rank.className = "player_name__rank"
    rank.innerHTML = `#${player.rank}`;
    wcl_link.appendChild(rank);

    let total = document.createElement("span");
    total.className = "player_name__total"
    total.innerHTML = player.total_fmt
    wcl_link.appendChild(total);

    return container
}



////////////////////////////////////////////////////////////////////////////////

export default class Scene {


    constructor(args) {

        this.spec_slug = args.spec_slug;
        this.boss_slug = args.boss_slug;

        // request results
        this.players = []

        // dict: applied filters
        this.filters = {}

        this.all_spells = {}
        this.used_spells = new Set();

        // Konva.Stage Subclass
        this.stage = new Stage({
            container: args.canvas
        });

        // HTML Elements
        this.player_names_container = args.player_names_container
        this.spell_settings_bar = args.spell_settings_bar
        this.loading_spinner = args.loading_spinner

        document.addEventListener("update_filter", event => {
            this.filters = {...this.filters, ...event.filters}
            this.update_filters()
        })

    }

    ////////////////////////////////////////////////////////////////////////////
    // loading

    create_player_names(players) {

        // remove any old divs
        this.player_names_container.innerHTML = '';

        // create html elements
        players.forEach(player => {
            let player_div = player.type == "boss" ? create_boss_name_div(player) : create_player_name_div(player)
            this.player_names_container.appendChild(player_div)
        })
    }

    init_players() {

        // collect players
        this.players = []
        this.fights_data.forEach((fight, i) => {

            // boss lane
            if (i == 0 && fight.boss) {
                let boss = fight.boss
                boss.type = "boss"
                boss.fight = fight
                this.players.push(boss)
            }

            // players
            fight.players.forEach(player => {
                player.fight = fight
                player.rank = i+1 // include from api?
                this.players.push(player)
            }) // for player
        }) // for fight

        // filter used spells
        this.used_spells.clear()
        this.players.forEach(player => {
            let cast_counter = {}
            player.casts.forEach(cast => {
                this.used_spells.add(cast.spell_id)

                cast_counter[cast.spell_id] = 1 + (cast_counter[cast.spell_id] || 0)
                cast.count = cast_counter[cast.spell_id]

            }) // for cast
        }) // for player
    }

    init_spells() {

        // setup spell buttons
        this.spells_data.forEach(spell => {

            // find the display button
            spell.button = this.spell_settings_bar.querySelector(`.button[data-spell_id="${spell.spell_id}"]`)
            if (!spell.button) {
                return
            }

            // show/hide if spell was used
            let was_used = this.used_spells.has(spell.spell_id)
            if (!was_used) {
                // we hide the parent link element
                hide(spell.button.parentElement)
                return;
            }

            spell.button.addEventListener("click", event => {
                spell.button.classList.toggle("disabled")
                let enabled = !spell.button.classList.contains("disabled")
                this.stage.show_spell(spell.spell_id, enabled)
            })
        })

        //////////////////////////////
        // setup spell groups

        this.spell_settings_bar.querySelectorAll(".group_header[data-spell_group]").forEach(header => {

            const group_name = header.dataset.spell_group;
            let group_buttons = document.querySelectorAll(`.settings_bar .button[data-spell_group="${group_name}"]`);

            header.addEventListener("click", event => {

                // flip this
                header.classList.toggle("disabled")
                let enabled = !header.classList.contains("disabled")
                console.log("group", group_name, enabled)

                // update all child buttons
                group_buttons.forEach(button => {
                    button.classList.toggle("disabled", !enabled);
                    this.stage.show_spell(button.dataset.spell_id, enabled)
                })
            })
        })

        document.addEventListener("toggle_cooldown", event => {
            this.stage.toggle_cooldown(event.show)
        })

        document.addEventListener("toggle_duration", event => {
            this.stage.toggle_duration(event.show)
        })

        document.addEventListener("toggle_casttime", event => {
            this.stage.toggle_casttime(event.show)
        })
    }

    async load() {

        // requests
        console.time("requests")
        let [fights_data, spells_data] = await Promise.all([
            load_fights(this.spec_slug, this.boss_slug),
            load_spells([this.spec_slug, this.boss_slug, "other-potions", "other-trinkets"])
        ])
        this.fights_data = fights_data // await
        this.spells_data = spells_data // await

        // this.fights_data = this.fights_data.slice(0, 10)

        console.timeEnd("requests")

        this.init_players()  // players first, so we are able to get "spells_used"
        this.init_spells()

        ////////////////////////////
        // Update the Stage

        console.time("stage set fights/spells")
        this.stage.set_spells(this.spells_data)
        this.stage.set_players(this.players)
        this.create_player_names(this.players)
        console.timeEnd("stage set fights/spells")

        this.update()
    }

    update() {

        show(this.loading_spinner)

        console.time("stage create")
        this.stage.create();
        console.timeEnd("stage create")
        console.time("stage update")
        this.stage.update();
        console.timeEnd("stage update")

        // Update Size
        this.stage.update_size()

        // hide spinner: delayed so the page can refresh first
        let s = this.loading_spinner
        setTimeout(function() {
            hide(s)
        }, 20)
    }

    ////////////////////////////////////////////////////////////////////////////
    // filters

    _filter_player(player) {

        // for now.. only the #1 fight has the boss lane
        if (player.type == "boss") {
            return true;
        }

        let fight = player.fight
        let fight_duration = fight.duration / 1000

        if (this.filters.killtime_min && this.filters.killtime_min > fight_duration) {
            return false
        }
        if (this.filters.killtime_max && this.filters.killtime_max < fight_duration) {
            return false
        }

        // exact check against false, as undefined is considered true in this case
        if ( this.filters[player.covenant] == false ) {
            return false
        }

        return true
    }

    update_filters() {

        show(this.loading_spinner)

        let players = this.players.filter(player => this._filter_player(player))

        this.stage.set_players(players)
        this.create_player_names(players)

        this.update()
    }
}
