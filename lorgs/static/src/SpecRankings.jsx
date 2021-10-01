

import React from 'react'
import { useParams } from 'react-router-dom';

import LoadingOverlay from "./components/shared/LoadingOverlay.jsx"
import PlayerNamesList from "./components/PlayerNames/PlayerNamesList.jsx"
import SettingsBar from "./components/SettingsBar/SettingsBar.jsx"
import TimelineCanvas from "./components/Timeline/TimelineCanvas.jsx"
import api from "./api.js"
import AppContext from "./AppContext/AppContext.jsx"
import { filter_unused_spells, apply_filters } from "./AppContext/filter_logic.js"


////////////////////////////////////////////////////////////////////////////////
// Fetch
//

/* Returns a list of fights
*/
async function load_spec_rankings(spec_slug, boss_slug) {

    let url = `/api/spec_ranking/${spec_slug}/${boss_slug}?limit=100`;
    let response = await fetch(url);
    if (response.status != 200) {
        return [];
    }
    const fight_data = await response.json();

    // post process
    return fight_data.fights.map((fight, i) => {
        fight.players.forEach(player => {
            player.rank = i+1  // insert ranking data
        })
        return fight
    })
}



////////////////////////////////////////////////////////////////////////////////
// Component
//

export default function SpecRankings() {

    const { spec_slug, boss_slug } = useParams();
    const app_data = AppContext.getData()

    // load data
    React.useEffect(async () => {

        // send requests
        console.time("requests")
        let spell_data = await api.load_spells([spec_slug, boss_slug, "other-potions", "other-trinkets"])
        const fights = await load_spec_rankings(spec_slug, boss_slug)
        console.timeEnd("requests")

        // update context
        app_data.spec_slug = spec_slug
        app_data.boss_slug = boss_slug
        app_data.spells = api.process_spells(spell_data)
        app_data.fights = fights
        app_data.spells = filter_unused_spells(app_data.spells, app_data.fights)
        app_data.is_loading = false
        app_data.refresh()


    }, [spec_slug, boss_slug])

    // always apply the current filters before rendering
    !app_data.is_loading && apply_filters(app_data.fights, app_data.filters)

    return (
        <div>

            <SettingsBar />
            {/* <div className={`${isLoading.current && "loading_trans"}`}></div> */}
            
            {app_data.is_loading && <LoadingOverlay />}

            <div className={`p-2 bg-dark rounded border d-flex overflow-hidden ${app_data.is_loading && "loading_trans"}`}>
                <PlayerNamesList />
                <TimelineCanvas />
            </div>
        </div>
    );
}
