
import React from 'react'
import { useParams } from 'react-router-dom';

import AppContext from "./../AppContext/AppContext.jsx"
import LoadingOverlay from "./../components/shared/LoadingOverlay.jsx"
import PlayerNamesList from "./../components/PlayerNames/PlayerNamesList.jsx"
import SettingsBar from "./../components/SettingsBar/SettingsBar.jsx"
import TimelineCanvas from "./../components/Timeline/TimelineCanvas.jsx"
import API from "./../api.js"


/* Returns a list of fights */
async function load_comp_rankings(boss_slug) {

    let url = `/api/comp_ranking/${boss_slug}`;
    let response = await fetch(url);
    if (response.status != 200) {
        return {};
    }
    const fight_data = await response.json();
    return fight_data
}



export default function CompRankings() {

    //////////////////////
    // inputs
    const { boss_slug } = useParams();
    const app_data = AppContext.getData()
    app_data.mode = AppContext.MODES.COMP_RANKING


    //////////////////////
    // load data
    React.useEffect(async () => {

        // send requests
        console.time("requests")
        
        const specs_dict = await API.load_specs({include_spells: true})
        app_data.specs = Object.values(specs_dict.specs)
        // let spell_data = await api.load_spells()
        const comp_rankings = await load_comp_rankings(boss_slug)
        console.timeEnd("requests")

        console.log("app_data.specs", app_data.specs)

        app_data.fights = comp_rankings.fights || []
        // app_data.spells = Object.values(spell_data)
        API.process_fetched_data(app_data)
        // app_data.specs = get_all_specs(app_data.fights)
        // app_data.filter_unused_spells()
        app_data.is_loading = false
        app_data.refresh()

    }, [boss_slug])


    //////////////////////
    // return
    return (
        <>
            <h1>Header: {app_data.boss.name}</h1>

            <div className={`${app_data.is_loading && "loading_trans"}`}>
                <SettingsBar />
            </div>

            {app_data.is_loading && <LoadingOverlay />}

            <div className={`p-2 bg-dark rounded border d-flex overflow-hidden ${app_data.is_loading && "loading_trans"}`}>
                <PlayerNamesList />
                <TimelineCanvas />
            </div>
        </>
    )
}
