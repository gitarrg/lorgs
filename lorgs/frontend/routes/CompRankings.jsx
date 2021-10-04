
import React from 'react'
import { useParams } from 'react-router-dom';
import { useSelector, batch } from 'react-redux'

import API from "./../api.js"
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

// TODO: move to API?
async function load_global_data() {
    const bosses = await API.load_bosses()
    data_store.dispatch({type: "update_value", field: "bosses", value: bosses})
    
    const roles = await API.load_roles()
    data_store.dispatch({type: "update_value", field: "roles", value: roles || []})

    // needs to rebuild when the nav bar changes
    ReactTooltip.rebuild()
}

async function load_comp_ranking_data(boss_slug) {
            // send requests
        console.time("load_data")
        data_store.dispatch({type: "update_value", field: "is_loading", value: true})

        // load boss
        const boss = await API.load_boss(boss_slug)
        
        // load specs
        const specs_dict = await API.load_specs({include_spells: true})
        const specs = specs_dict.specs

        // fights
        const comp_rankings = await load_comp_rankings(boss_slug)
        const fights = comp_rankings.fights || []

        batch(() => {

            // set all new values
            data_store.dispatch({type: "update_value", field: "boss", value: boss})
            data_store.dispatch({type: "update_value", field: "specs", value: specs})
            data_store.dispatch({type: "update_value", field: "fights", value: fights})

            // apply some processing
            data_store.dispatch({type: "process_fetched_data"})
            data_store.dispatch({type: "filters/apply"})

            // mark as loaded
            data_store.dispatch({type: "update_value", field: "is_loading", value: false})
        })
        console.timeEnd("load_data")
}


////////////////////////////////////////////////////////////////////////////////
// Component
//


export default function CompRankings() {

    //////////////////////
    // inputs
    const { boss_slug } = useParams();

    // const state = data_store.getState()
    const is_loading = useSelector(state => state.is_loading)


    //////////////////////
    // load data

    /* load global data */
    React.useEffect(async () => {
        data_store.dispatch({type: "update_value", field: "mode", value: MODES.COMP_RANKING})
        await load_global_data()
    }, [])

    React.useEffect(async () => {
        await load_comp_ranking_data(boss_slug)
    }, [boss_slug])


    //////////////////////
    // return
    return (
        <>
            <div className="mt-3 flex-row d-flex flex-wrap-reverse">
                <Header />
                <Navbar />
            </div>

            <div className={`${is_loading ? "loading_trans" : ""}`}>
                <SettingsBar />
            </div>

            {is_loading && <LoadingOverlay />}

            <div className={`p-2 bg-dark rounded border d-flex overflow-hidden ${is_loading && "loading_trans"}`}>
                <PlayerNamesList />
                <TimelineCanvas />
            </div>
        </>
    )
}
