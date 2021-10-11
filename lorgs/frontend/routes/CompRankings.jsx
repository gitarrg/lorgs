
import React from 'react'
import { useParams, useLocation } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux'

import * as ui_store from "../store/ui.js"
import CompRankingsHeader from './CompRankings/CompRankingsHeader.jsx';
import CompSettingsBar from './CompRankings/CompSettingsBar.jsx';
import LoadingOverlay from "./../components/shared/LoadingOverlay.jsx"
import Navbar from "./../components/Navbar/Navbar.jsx"
import PlayerNamesList from "./../components/PlayerNames/PlayerNamesList.jsx"
import TimelineCanvas from "./../components/Timeline/TimelineCanvas.jsx"
import { get_boss } from '../store/bosses.js';
import { load_fights } from '../store/fights.js';


const INITIAL_FILTERS = {

    // hide raid cd's by default
    class: {
        "warrior": false,
        "deathknight": false,
        "demonhunter": false,
    }

}


function update_title(boss) {
    if (!boss) { return }
    document.title = `Lorrgs: Comp Ranking: ${boss.full_name}`
}


export default function CompRankings() {

    ////////////////////////////////////////////////////////////////////////////
    // Hooks
    const { boss_slug } = useParams();
    const dispatch = useDispatch()
    const { search } = useLocation();
    const is_loading = useSelector(state => ui_store.get_is_loading(state))
    const boss = useSelector(state => get_boss(state, boss_slug))

    // const
    const mode = ui_store.MODES.COMP_RANKING

    ////////////////////////////////////////////////////////////////////////////
    // Update State
    //

    /* set current mode */
    // initial page values
    React.useEffect(() => {
        dispatch(ui_store.set_mode(mode))
        dispatch(ui_store.set_filters(INITIAL_FILTERS))
    }, [])

    React.useEffect(() => { dispatch(ui_store.set_values({boss_slug: boss_slug})) }, [boss_slug])

    // update title once boss & spec are loaded
    React.useEffect(() => { update_title(boss)  }, [boss])

    // load
    React.useEffect(() => { dispatch(load_fights(mode, {boss_slug, search})) }, [boss_slug, search])


    ////////////////////////////////////////////////////////////////////////////
    // Render
    return (
        <>
            <div className="mt-3 flex-row d-flex flex-wrap-reverse">
                <CompRankingsHeader />
                <Navbar />
            </div>

            <div className={`${is_loading ? "loading_trans" : ""}`}>
                <CompSettingsBar />
            </div>

            {is_loading && <LoadingOverlay />}

            <div className={`p-2 bg-dark rounded border d-flex overflow-hidden ${is_loading && "loading_trans"}`}>
                <PlayerNamesList />
                <TimelineCanvas />
            </div>
        </>
    )
}
