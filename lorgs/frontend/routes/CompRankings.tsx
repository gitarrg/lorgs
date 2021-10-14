
import React from 'react'
import { useParams, useLocation } from 'react-router-dom';
import { useSelector, useDispatch, batch } from 'react-redux'

import * as ui_store from "../store/ui"
import CompRankingsHeader from './CompRankings/CompRankingsHeader';
import CompSettingsBar from './CompRankings/CompSettingsBar';
import LoadingOverlay from "./../components/shared/LoadingOverlay"
import Navbar from "./../components/Navbar/Navbar"
import PlayerNamesList from "./../components/PlayerNames/PlayerNamesList"
import TimelineCanvas from "./../components/Timeline/TimelineCanvas"
import { get_boss, load_boss_spells } from '../store/bosses';
import { load_fights } from '../store/fights';
import { load_spec_spells } from '../store/specs';


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

        batch(() => { // does this even do anything?
            // mode
            dispatch(ui_store.set_mode(mode))
            dispatch(ui_store.set_filters(INITIAL_FILTERS))

            // Healers
            dispatch(load_spec_spells("paladin-holy"))
            dispatch(load_spec_spells("priest-holy"))
            dispatch(load_spec_spells("priest-discipline"))
            dispatch(load_spec_spells("shaman-restoration"))
            dispatch(load_spec_spells("monk-mistweaver"))
            dispatch(load_spec_spells("druid-restoration"))

            // Classes wth Raid CDs
            dispatch(load_spec_spells("deathknight-unholy"))
            dispatch(load_spec_spells("warrior-fury"))
            dispatch(load_spec_spells("demonhunter-havoc"))
        }) // batch
    }, [])


    React.useEffect(() => { dispatch(ui_store.set_boss_slug(boss_slug)) }, [boss_slug])

    // update title once boss & spec are loaded
    React.useEffect(() => { update_title(boss)  }, [boss])

    // load boss spells, once boss is loaded
    React.useEffect(() => {
        if (!boss) { return }
        if (boss.loaded) { return } // skip if we already have them
        dispatch(load_boss_spells(boss.full_name_slug))
    }, [boss])

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

            <div className={`p-2 bg-dark rounded border d-flex ${is_loading ? "loading_trans" : ""}`}>
                <PlayerNamesList />
                <TimelineCanvas />
            </div>
        </>
    )
}
