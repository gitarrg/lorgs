
import React, { useState, useContext } from "react"
import useFetch from "react-fetch-hook";


import PlayerNamesList from "./components/PlayerNamesList.jsx"
import TimelineCanvas from "./components/TimelineCanvas.jsx"
import AppDataContext, { DEFAULT_CONTEXT } from "./AppDataContext.jsx"


// export const AppDataContext = React.createContext()
// import { CONTEXT } from "./constants.jsx";

console.log("loading app.js")


async function load_fights(spec_slug, boss_slug) {

    let url = `/api/spec_ranking/${spec_slug}/${boss_slug}?limit=10`;
    let response = await fetch(url);
    if (response.status != 200) {
        return;
    }
    let data = await response.json();
    return data.fights;
}


/* function create_default_players(spec_slug, n) {
    const default_players = []
    for (let i = 0; i < n; i++) {
        let player = {
            "name": `player_${i}`,
            "rank": i+1,
            "total": 0,
            "spec_slug": spec_slug,
            "class_slug": spec_slug.split("-")[0],
            "fight": {},
        }
        default_players.push(player)
    }

    return default_players
} */


function process_spells(spellsData) {

    let new_spells = Object.values(spellsData)
    new_spells.forEach(spell => {

        // this is a bit of a hack... 
        // we reuse the img from the settings bar
        spell.image = document.querySelector(`.button[data-spell_id="${spell.spell_id}"]`)
    })
    // setSpells(new_spells)
    return new_spells
    // let new_context = {...context, spells: new_spells}
    // setContext(new_context)
}


function process_fights(fightsData) {

    let main_fight = {}
    main_fight.players = []
    fightsData.fights.forEach((fight, i) => {
        fight.players.forEach(player => {
            player.rank = i+1
            player.fight = fight
            main_fight.players.push(player)
        });
    })

    return [main_fight]
    // let new_context = {...context, fights: [main_fight]}
    // setContext(new_context)
}




export default function App(props) {



    const settings = props.settings
    const spec_slug = settings.spec_slug
    const boss_slug = settings.boss_slug

    console.log("app main", settings)

    const [context, setContext] = React.useState(DEFAULT_CONTEXT)

    const [spells, setSpells] = React.useState([])
    const [fights, setFights] = React.useState([])

    let groups = [spec_slug, boss_slug, "other-potions", "other-trinkets"]
    let params = new URLSearchParams(groups.map(g => ["group", g]))
    const fightsData = useFetch(`/api/spec_ranking/${spec_slug}/${boss_slug}?limit=10`);
    const spellsData = useFetch(`/api/spells?${params}`);


    // create/fill the app context
    // let context = {} // {"more": [1, 2, 3]}
    // context.zoom = zoom
    // context.spells = spellsData.data



    // React.useEffect(process_spells, [spellsData.data])

/*     function process_fights() {
        if (fightsData.isLoading) {return}

        let main_fight = {}
        main_fight.players = []
        fightsData.data.fights.forEach((fight, i) => {
            fight.players.forEach(player => {
                player.rank = i+1
                player.fight = fight
                main_fight.players.push(player)
            });
        })

        let new_context = {...context, fights: [main_fight]}
        setContext(new_context)
    } */
    // React.useEffect(process_fights, [fightsData.data])
   

    /*     async function load_new_fights() {
        let fights_data = await load_fights(spec_slug, boss_slug)
        
        let new_players = []
        fights_data.forEach((fight, i) => {
            fight.players.forEach(player => {
                player.fight = fight
                player.rank = i + 1 // include from api?
                new_players.push(player)
            })
        })
        // setDuration(300)
        // setPlayers(new_players)
        return new_players
    } */
    //players.current = await load_new_fights()
    // console.log("players", players.current)

    // React.useEffect(() => {}, [])
    // let x = setAppData()
    // x({"new": 8})

    if (fightsData.isLoading || spellsData.isLoading) {
        return <div>Loading...</div>
    }

    let new_context = {...context}
    new_context["spells"] = process_spells({...spellsData.data})
    new_context["fights"] = process_fights({...fightsData.data})

    return (
        <React.Fragment>
            <AppDataContext.Provider value={new_context}>

                <PlayerNamesList />
                <TimelineCanvas />

            </AppDataContext.Provider>
        </React.Fragment>
    )

}


if (SETTINGS) {
    ReactDOM.render(
        <App settings={SETTINGS}/>,
        document.getElementById("app_root")
    );
}



