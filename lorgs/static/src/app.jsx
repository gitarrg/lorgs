
import React, { useState, useContext } from "react"
import useFetch from "react-fetch-hook";


import PlayerNamesList from "./components/PlayerNamesList.jsx"
import TimelineCanvas from "./components/TimelineCanvas.jsx"
import AppDataContext from "./AppDataContext.jsx"


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





export default function App() {

    // TODO: replace test values
    const spec_slug = "shaman-restoration"
    const boss_slug = "painsmith-raznal"

    console.log("app main")
    
    const players = React.useRef([])
    const [duration, setDuration] = React.useState(0)
    const [zoom, setZoom] = React.useState(4)

    let groups = [spec_slug, boss_slug, "other-potions", "other-trinkets"]
    let params = new URLSearchParams(groups.map(g => ["group", g]))
    const spellsData = useFetch(`/api/spells?${params}`);
    
    const fightsData = useFetch(`/api/spec_ranking/${spec_slug}/${boss_slug}?limit=10`);

   
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

    function updateScale(e) {
        let input = e.target
        console.log("updateScale", input.value)
        setZoom(input.value)
    }

    // create/fill the app context
    let context = {} // {"more": [1, 2, 3]}
    context.zoom = zoom
    context.spells = spellsData.data

    let new_players = []
    fightsData.data.fights.forEach((fight, i) => {
        fight.players.forEach(player => {
            player.fight = fight
            player.rank = i + 1 // include from api?
            new_players.push(player)
        })
    })
    
    return (
        <React.Fragment>
            <input type="range" min="0.1" max="11" step="0.1" onChange={updateScale} />
         
            <AppDataContext.Provider value={context}>
                <PlayerNamesList players={new_players} />
                <TimelineCanvas players={new_players} duration={duration}/>
            </AppDataContext.Provider>
        </React.Fragment>
    )

}


ReactDOM.render(
    <App />,
    document.getElementById("app_root")
);


