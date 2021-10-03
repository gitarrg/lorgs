
import React from 'react'
import { useParams } from 'react-router-dom';

import API from "./../api.js"
import AppContext from "./../AppContext/AppContext.jsx"
import Header from "./../components/Header.jsx"
import LoadingOverlay from "./../components/shared/LoadingOverlay.jsx"
import Navbar from "./../components/Navbar/Navbar.jsx"
import PlayerNamesList from "./../components/PlayerNames/PlayerNamesList.jsx"
import SettingsBar from "./../components/SettingsBar/SettingsBar.jsx"
import TimelineCanvas from "./../components/Timeline/TimelineCanvas.jsx"
import data_store, { MODES } from '../data_store.js'


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

    const state = data_store.getState()
    state.mode = MODES.COMP_RANKING


    //////////////////////
    // load data

    /* load global data */
    React.useEffect(async () => {
        const bosses = await API.load_bosses()
        data_store.dispatch({type: "update_value", field: "bosses", value: bosses})
        console.log("load global data")
    })

    React.useEffect(async () => {
        // send requests
        console.time("requests")

        const boss = await API.load_boss(boss_slug)
        data_store.dispatch({type: "update_value", field: "boss", value: boss})

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

            <div className="mt-3 flex-row d-flex flex-wrap-reverse">
                <Header />
                <Navbar />
            </div>

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
