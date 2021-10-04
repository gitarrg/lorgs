

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

////////////////////////////////////////////////////////////////////////////////
// Fetch
//


async function load_global_data() {
    const bosses = await API.load_bosses()
    data_store.dispatch({type: "update_value", field: "bosses", value: bosses})
    
    const roles = await API.load_roles()
    data_store.dispatch({type: "update_value", field: "roles", value: roles || []})
}


async function load_spec_ranking_data(spec_slug, boss_slug) {

    console.log("load_data start")
    console.time("load_data")

    data_store.dispatch({type: "update_value", field: "is_loading", value: true})

    // load boss
    const boss = await API.load_boss(boss_slug)
    
    // load spec (+extra specs)
    const specs = await API.load_multiple_specs([spec_slug, "other-potions", "other-trinkets"])
    const [spec] = [...specs]
    
    // fights
    const fights = await API.load_spec_rankings(spec_slug, boss_slug)
    
    batch(() => {

        // set all new values
        data_store.dispatch({type: "update_value", field: "boss", value: boss})
        data_store.dispatch({type: "update_value", field: "spec", value: spec})
        data_store.dispatch({type: "update_value", field: "specs", value: specs})
        data_store.dispatch({type: "update_value", field: "fights", value: fights})
        
        // apply some processing
        data_store.dispatch({type: "process_fetched_data"})
        data_store.dispatch({type: "filters/apply"})

        // mark as loaded
        data_store.dispatch({type: "update_value", field: "is_loading", value: false})
    })

    // await new Promise(r => setTimeout(r, 2000));
    console.timeEnd("load_data")
}


////////////////////////////////////////////////////////////////////////////////
// Component
//

export default function SpecRankings() {

    const { spec_slug, boss_slug } = useParams();

    // new state
    const state = data_store.getState()
    state.mode = MODES.SPEC_RANKING // use dispatch?

    const is_loading = useSelector(state => state.is_loading)

    /* load global data */
    React.useEffect(load_global_data, [])

    React.useEffect(async () => {
        await load_spec_ranking_data(spec_slug, boss_slug)
    }, [spec_slug, boss_slug])

    return (
        <div>

            <div className="mt-3 flex-row d-flex flex-wrap-reverse">
                <Header />
                <Navbar />
            </div>

            <div className={`${is_loading && "loading_trans"}`}>
                <SettingsBar />
            </div>
            
            {is_loading && <LoadingOverlay />}

            <div className={`p-2 bg-dark rounded border d-flex overflow-hidden ${is_loading && "loading_trans"}`}>
                <PlayerNamesList />
                <TimelineCanvas />
            </div>
        </div>
    );
}
