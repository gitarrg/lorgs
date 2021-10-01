
import React  from "react"

import AppDataContext, { DEFAULT_CONTEXT } from "./AppDataContext.jsx"
import LoadingOverlay from "./components/LoadingOverlay.jsx"
import PlayerNamesList from "./components/PlayerNames/PlayerNamesList.jsx"
import SettingsBar from "./components/SettingsBar/SettingsBar.jsx"
import TimelineCanvas from "./components/TimelineCanvas.jsx"



const ICON_ROOT = "https://wow.zamimg.com/images/wow/icons/medium"


////////////////////////////////////////////////////////////////////////////////
//
//

async function load_spells(groups) {

    let params = new URLSearchParams(groups.map(g => ["group", g]))
    let url ="/api/spells?" + params

    let response = await fetch(url);
    if (response.status != 200) {
        return []
    }
    let data = await response.json()
    return data

    // convert into regular list
    // this is probl not needed.. but idk..
    let spells = []
    for(var i in data) {
        spells.push(data[i])
    }
    return spells;
}


async function load_fights(spec_slug, boss_slug) {

    let url = `/api/spec_ranking/${spec_slug}/${boss_slug}?limit=100`;
    let response = await fetch(url);
    if (response.status != 200) {
        return;
    }
    return await response.json();
}


function process_spells(spellsData) {
    let spells = Object.values(spellsData)

    spells.forEach(spell => {

        spell.icon_path = spell.icon.startsWith("/") ? spell.icon : `${ICON_ROOT}/${spell.icon}`

        // kind of shit.. but better then setting up all the callback stuff for image loading in konva
        spell.image = document.createElement("img")
        spell.image.src = spell.icon_path
    })

    return spells;
}


function process_fights(fightsData) {

    // let main_fight = {}
    // main_fight.players = []
    let fights = []
    fightsData.fights.forEach((fight, i) => {
        fight.players.forEach(player => {
            player.rank = i+1
            // player.fight = fight
            // main_fight.players.push(player)
        });
        fights.push(fight)
    })
    return fights
}


////////////////////////////////////////////////////////////////////////////////
//
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

function create_random_player(spec_slug) {

    return {
        "name": "",
        "rank": -1,
        "total": randint(250, 20000),
        // "spec_slug": spec_slug,
        // "class_slug": spec_slug.split("-")[0],
        "casts": create_random_casts(),
    }
}

function create_default_fights(spec_slug, n) {


    let fights = []

    for (let i = 0; i < n; i++) {
        let fight = {}
        fight.loading = true
        fight.duration = 1000 * randint(120, 240)
        fight.players = [create_random_player(spec_slug)]
        fight.report_id = `dummy_${i}`
        fights.push(fight)
    }
    return fights
}


function create_default_context(spec_slug, boss_slug) {

    let context = {...DEFAULT_CONTEXT}

    context.spells = {}
    context.spells[0] = {"spell_id": 0, "color": "#ccc", "duration": 30, "show": true}

    context.fights = create_default_fights(spec_slug, 20)
    return context
}


////////////////////////////////////////////////////////////////////////////////
// FILTERS
//

function spell_was_used(spell, fights) {




}

function filter_unused_spells(context) {

    let used_spells = new Set()
    context.fights.forEach(fight => {

        if (fight.boss && fight.boss.casts) {
            fight.boss.casts.forEach(cast => {
                used_spells.add(cast.id)
            })
        }

        (fight.players || []).forEach(player => {
            (player.casts || []).forEach(cast => {
                used_spells.add(cast.id)
            })
        })
    })
    console.log(used_spells)
    context.spells = context.spells.filter(spell => used_spells.has(spell.spell_id))
}


function apply_filters_fight(fight, filters) {
    let fight_duration = fight.duration / 1000
    if (filters.killtime_min && filters.killtime_min > fight_duration) {
        return false
    }
    if (filters.killtime_max && filters.killtime_max < fight_duration) {
        return false
    }
    return true
}

function apply_filters_player(player, filters) {

    // exact check against false, as undefined is considered true in this case
    if ( filters[player.covenant] === false ) {
        return false
    }
    return true
}

function apply_filters(fights, filters) {

    fights.forEach((fight, f) => {
        fight.visible = apply_filters_fight(fight, filters)

        if (fight.boss) {
            fight.boss.visible = true  // FIXME
        }

        if (fight.visible) {
            fight.players.forEach(player => {
                player.visible = apply_filters_player(player, filters)
            })
        }

        fight.visible = fight.visible && fight.players.some(player => player.visible)

    })
}



////////////////////////////////////////////////////////////////////////////////
// APP
//

export default function App(props) {


    const settings = props.settings
    const spec_slug = settings.spec_slug
    const boss_slug = settings.boss_slug

    const isLoading = React.useRef(true)
    const [context, setContext] = React.useState(() => create_default_context(spec_slug, boss_slug))
    context.setContext = setContext

    // const [spells, setSpells] = React.useState([])
    // const [fights, setFights] = React.useState([])

    // const fightsData = useFetch(`/api/spec_ranking/${spec_slug}/${boss_slug}`);
    // const spellsData = useFetch(`/api/spells?${params}`);

    // load data
    React.useEffect(async () => {

        // send requests
        console.time("requests")
        let spell_data = await load_spells([spec_slug, boss_slug, "other-potions", "other-trinkets"])
        let fight_data = await load_fights(spec_slug, boss_slug)
        console.timeEnd("requests")

        // update context
        let new_context = {...context}
        new_context.spec_slug = spec_slug
        new_context.boss_slug = boss_slug
        new_context.spells = process_spells(spell_data)
        new_context.fights = process_fights(fight_data)

        filter_unused_spells(new_context)


        // apply_filters(new_context.fights, new_context.filters)

        // trigger rerender
        isLoading.current = false
        setContext(new_context)
        // hide(document.getElementById("canvas_loading"))
    }, [spec_slug, boss_slug])


    // always apply the current filters before rendering
    apply_filters(context.fights, context.filters)


    ////////////////////////
    // Output

    return (
        <React.StrictMode>
            <AppDataContext.Provider value={context}>

            <React.Fragment>

                <div className={`${isLoading.current && "loading_trans"}`}>
                    <SettingsBar />
                </div>

                {isLoading.current && <LoadingOverlay />}
                <div className={`p-2 bg-dark rounded border d-flex overflow-hidden ${isLoading.current && "loading_trans"}`}>
                    <PlayerNamesList />
                    <TimelineCanvas />
                </div>

            </React.Fragment>
            </AppDataContext.Provider>
        </React.StrictMode>
    )

}


if (SETTINGS) {
    ReactDOM.render(
        <App settings={SETTINGS}/>,
        document.getElementById("app_root")
    );
}



