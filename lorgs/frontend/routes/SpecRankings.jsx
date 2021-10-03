

import React from 'react'
import { useParams } from 'react-router-dom';

import AppContext from "./../AppContext/AppContext.jsx"
import Header from "./../components/Header.jsx"
import LoadingOverlay from "./../components/shared/LoadingOverlay.jsx"
import Navbar from "./../components/Navbar/Navbar.jsx"
import PlayerNamesList from "./../components/PlayerNames/PlayerNamesList.jsx"
import SettingsBar from "./../components/SettingsBar/SettingsBar.jsx"
import TimelineCanvas from "./../components/Timeline/TimelineCanvas.jsx"
import API from "./../api.js"
import { apply_filters } from "./../AppContext/filter_logic.js"
import data_store, { MODES } from '../data_store.js'

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

    // old context
    const app_data = AppContext.getData()
    app_data.mode = AppContext.MODES.SPEC_RANKING
    app_data.spec_slug = spec_slug
    app_data.boss_slug = boss_slug
    
    // new state
    const state = data_store.getState()
    state.mode = MODES.SPEC_RANKING

    // load data

    /* load global data */
    React.useEffect(async () => {
        const bosses = await API.load_bosses()
        data_store.dispatch({type: "update_value", field: "bosses", value: bosses})
        
        const roles = await API.load_roles()
        console.log("roles", roles)
        data_store.dispatch({type: "update_value", field: "roles", value: roles.roles || []})
    }, [])


    React.useEffect(async () => {

        // send requests  TODO: wrap into a await all group
        console.time("requests")

        app_data.specs = await API.load_multiple_specs([spec_slug, "other-potions", "other-trinkets"])
        console.log("app_data.specs", app_data.specs)

        app_data.boss = await API.load_boss(boss_slug),
        app_data.fights = await load_spec_rankings(spec_slug, boss_slug)

        const spec = app_data.specs[0]
        data_store.dispatch({type: "update_value", field: "spec", value: spec})
        data_store.dispatch({type: "update_value", field: "boss", value: app_data.boss})

        console.timeEnd("requests")

        // update context
        API.process_fetched_data(app_data)
        app_data.is_loading = false
        app_data.refresh()


    }, [spec_slug, boss_slug])

    // always apply the current filters before rendering
    !app_data.is_loading && apply_filters(app_data.fights, app_data.filters)

    return (
        <div>

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
        </div>
    );
}
