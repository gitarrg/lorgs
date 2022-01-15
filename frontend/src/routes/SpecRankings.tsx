
import { useDispatch } from 'react-redux'
import { useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { useTitle } from 'react-use'

import * as ui_store from "../store/ui"
import LoadingOverlay from "./../components/shared/LoadingOverlay"
import Navbar from "./../components/Navbar/Navbar"
import PlayerNamesList from "./../components/PlayerNames/PlayerNamesList"
import SpecRankingsHeader from './SpecRankings/SpecRankingsHeader'
import SpecSettingsBar from './SpecRankings/SpecSettingsBar'
import TimelineCanvas from "./../components/Timeline/TimelineCanvas"
import { get_boss, load_boss_spells } from '../store/bosses'
import { get_spec, load_spec_spells } from '../store/specs'
import { load_fights } from "../store/fights"
import { useAppSelector } from '../store/store_hooks'


////////////////////////////////////////////////////////////////////////////////
// Component
//

export default function SpecRankings() {

    ////////////////////////////////////////////////////////////////////////////
    // Hooks
    const { spec_slug, boss_slug, difficulty="mythic" } = useParams<{spec_slug: string, boss_slug: string, difficulty: string}>();
    const dispatch = useDispatch()
    const is_loading = useAppSelector(state => ui_store.get_is_loading(state))
    const boss = useAppSelector(state => get_boss(state, boss_slug))
    const spec = useAppSelector(state => get_spec(state, spec_slug))

    // const
    const mode = ui_store.MODES.SPEC_RANKING

    ////////////////////////////////////////////////////////////////////////////
    // Update State
    //
    useTitle(`Lorrgs: ${spec?.full_name || "..."} vs. ${boss?.full_name || "..."}`)

    // set UI values
    useEffect(() => { dispatch(ui_store.set_mode(mode)) }, [])
    useEffect(() => { dispatch(ui_store.set_boss_slug(boss_slug)) }, [boss_slug])
    useEffect(() => { dispatch(ui_store.set_spec_slug(spec_slug)) }, [spec_slug])
    useEffect(() => { dispatch(ui_store.set_difficulty(difficulty)) }, [difficulty])

    useEffect(() => {
        if (!spec) { return }
        if (spec.loaded) { return } // skip if we already have them
        dispatch(load_spec_spells(spec.full_name_slug))
    }, [spec])

    useEffect(() => {
        if (!boss) { return }
        if (boss.loaded) { return } // skip if we already have them
        dispatch(load_boss_spells(boss.full_name_slug))
    }, [boss])

    // load fights
    useEffect(() => {
        dispatch(load_fights(mode, {spec_slug, boss_slug, difficulty}))
    }, [spec_slug, boss_slug, difficulty])


    ////////////////////////////////////////////////////////////////////////////
    // Render
    //
    return (
        <div className={mode}>

            <div className="mt-3 flex-row d-flex flex-wrap-reverse">
                <SpecRankingsHeader spec_slug={spec_slug} boss_slug={boss_slug} />
                <Navbar />
            </div>

             <div className={`${is_loading ? "loading_trans" : ""}`}>
                <SpecSettingsBar />
            </div>
            {is_loading && <LoadingOverlay />}

            <div className={`p-2 bg-dark rounded border d-flex ${is_loading ? "loading_trans" : ""}`}>
                <PlayerNamesList />
                <TimelineCanvas />
            </div>
        </div>
    );
}
