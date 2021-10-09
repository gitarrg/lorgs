
import React from 'react'
import { useParams, useLocation } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux'

import * as ui_store from "../store/ui.js"
import CompSettingsBar from './CompRankings/CompSettingsBar.jsx';
import Header from "./../components/Header.jsx"
import LoadingOverlay from "./../components/shared/LoadingOverlay.jsx"
import Navbar from "./../components/Navbar/Navbar.jsx"
import PlayerNamesList from "./../components/PlayerNames/PlayerNamesList.jsx"
import TimelineCanvas from "./../components/Timeline/TimelineCanvas.jsx"
import { load_fights } from '../store/fights.js';



export default function CompRankings() {

    ////////////////////////////////////////////////////////////////////////////
    // Hooks
    const { boss_slug } = useParams();
    const dispatch = useDispatch()
    const { search } = useLocation();
    const is_loading = useSelector(state => state.ui.is_loading)
    const mode = ui_store.MODES.COMP_RANKING

    ////////////////////////////////////////////////////////////////////////////
    // Update State
    //

    /* set current mode */
    React.useEffect(() => {
        dispatch(ui_store.set_mode(mode))
    }, [])

    // set current boss
    React.useEffect(() => {
        dispatch(ui_store.set_values({boss_slug: boss_slug}))
    }, [boss_slug])


    React.useEffect(async () => {
        dispatch(load_fights(mode, {boss_slug, search}))
    }, [boss_slug, search])


    ////////////////////////////////////////////////////////////////////////////
    // Render
    return (
        <>
            <div className="mt-3 flex-row d-flex flex-wrap-reverse">
                <Header />
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
