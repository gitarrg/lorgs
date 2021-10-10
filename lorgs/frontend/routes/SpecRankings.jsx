

import React from 'react'
import { useParams } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux'

import * as ui_store from "../store/ui.js"
import LoadingOverlay from "./../components/shared/LoadingOverlay.jsx"
import Navbar from "./../components/Navbar/Navbar.jsx"
import PlayerNamesList from "./../components/PlayerNames/PlayerNamesList.jsx"
import SpecSettingsBar from './SpecRankings/SpecSettingsBar.jsx';
import TimelineCanvas from "./../components/Timeline/TimelineCanvas.jsx"
import { load_fights } from "../store/fights.js"
import SpecRankingsHeader from './SpecRankings/SpecRankingsHeader.jsx';
// import { load_spec } from "../store/specs.js"
// import { load_spells } from '../store/spells.js';



////////////////////////////////////////////////////////////////////////////////
// Component
//

export default function SpecRankings() {

    ////////////////////////////////////////////////////////////////////////////
    // Hooks
    const { spec_slug, boss_slug } = useParams();
    const dispatch = useDispatch()
    const is_loading = useSelector(state => state.ui.is_loading)
    const mode = ui_store.MODES.SPEC_RANKING

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

    // load and set current spec
    React.useEffect(() => {
        // dispatch(load_spec(spec_slug))
        dispatch(ui_store.set_values({spec_slug: spec_slug}))
    }, [spec_slug])

    // load fights
    React.useEffect(() => {
        dispatch(ui_store.set_values({is_loading: true}))
        dispatch(load_fights(mode, {spec_slug, boss_slug}))
    }, [spec_slug, boss_slug])


    ////////////////////////////////////////////////////////////////////////////
    // Render
    //
    return (
        <div>

            <div className="mt-3 flex-row d-flex flex-wrap-reverse">
                <SpecRankingsHeader spec_slug={spec_slug} />
                <Navbar />
            </div>

             <div className={`${is_loading ? "loading_trans" : ""}`}>
                <SpecSettingsBar />
            </div>
            {is_loading && <LoadingOverlay />}

            <div className={`p-2 bg-dark rounded border d-flex overflow-hidden ${is_loading && "loading_trans"}`}>
                <PlayerNamesList />
                <TimelineCanvas />
            </div>
        </div>
    );
}
