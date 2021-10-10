

import React from 'react'
import { useParams } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux'

import * as ui_store from "../store/ui.js"
import LoadingOverlay from "./../components/shared/LoadingOverlay.jsx"
import Navbar from "./../components/Navbar/Navbar.jsx"
import PlayerNamesList from "./../components/PlayerNames/PlayerNamesList.jsx"
import SpecRankingsHeader from './SpecRankings/SpecRankingsHeader.jsx';
import SpecSettingsBar from './SpecRankings/SpecSettingsBar.jsx';
import TimelineCanvas from "./../components/Timeline/TimelineCanvas.jsx"
import { load_fights } from "../store/fights.js"
import { get_boss } from '../store/bosses.js';
import { get_spec } from '../store/specs.js';


function update_title(boss, spec) {
    if (!boss || !spec) { return }
    document.title = `Lorrgs: ${spec.full_name} vs. ${boss.full_name}`
}



////////////////////////////////////////////////////////////////////////////////
// Component
//

export default function SpecRankings() {

    ////////////////////////////////////////////////////////////////////////////
    // Hooks
    const { spec_slug, boss_slug } = useParams();
    const dispatch = useDispatch()
    const is_loading = useSelector(state => ui_store.get_is_loading(state))
    const boss = useSelector(state => get_boss(state, boss_slug))
    const spec = useSelector(state => get_spec(state, spec_slug))

    console.log("is_loading", is_loading)

    // const
    const mode = ui_store.MODES.SPEC_RANKING

    ////////////////////////////////////////////////////////////////////////////
    // Update State
    //

    /* set UI values */
    React.useEffect(() => { dispatch(ui_store.set_mode(mode)) }, [])
    React.useEffect(() => { dispatch(ui_store.set_values({boss_slug: boss_slug})) }, [boss_slug])
    React.useEffect(() => { dispatch(ui_store.set_values({spec_slug: spec_slug})) }, [spec_slug])

    // update title once boss & spec are loaded
    React.useEffect(() => { update_title(boss, spec)  }, [boss, spec])

    // load fights
    React.useEffect(() => {
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
