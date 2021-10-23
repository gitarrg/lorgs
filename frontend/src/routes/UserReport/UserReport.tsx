import { useDispatch } from 'react-redux'
import { useEffect } from 'react'
import { useParams, useLocation } from 'react-router-dom'
import { useTitle } from 'react-use'

import * as ui_store from "../../store/ui"
import LoadingOverlay from "./../../components/shared/LoadingOverlay"
import PlayerNamesList from "./../../components/PlayerNames/PlayerNamesList"
import TimelineCanvas from "./../../components/Timeline/TimelineCanvas"
import { get_spec, load_spec_spells } from '../../store/specs'
import { useAppSelector } from '../../store/store_hooks'
import ReportHeader from './ReportHeader'
import ReportSettingsBar from './ReportSettingsBar'
import { load_report_overview, set_report_id } from '../../store/user_reports'

import { get_occuring_specs, load_report_fights } from "../../store/fights"
import ReportNavbar from './ReportNavbar'



////////////////////////////////////////////////////////////////////////////////
// Component
//

export default function UserReport() {

    ////////////////////////////////////////////////////////////////////////////
    // Hooks
    const { report_id } = useParams<{report_id: string}>();
    const { search } = useLocation();

    const dispatch = useDispatch()
    const is_loading = useAppSelector(state => ui_store.get_is_loading(state))
    const specs = useAppSelector(state => get_occuring_specs(state))


    const mode = ui_store.MODES.USER_REPORT

    ////////////////////////////////////////////////////////////////////////////
    // Update State
    //
    useTitle(`Lorrgs: Report: ${report_id}`)

    useEffect(() => {
        dispatch(ui_store.set_mode(mode)) // in useEffect to only run once
    }, [])

    useEffect(() => {
        dispatch(load_report_overview(report_id))
        dispatch(load_report_fights(report_id))
    }, [report_id])

    // update player and fight selection
    useEffect(() => {
        const search_params = new URLSearchParams(search)
        const fight_ids: number[] = search_params.getAll("fight").map(v => parseInt(v))
        const player_ids: number[] = search_params.getAll("player").map(v => parseInt(v))

        dispatch(ui_store.set_filters({
            player_ids,
            fight_ids,
        }))
    }, [search])

    useEffect(() => {
        specs.forEach(spec_slug => {
            dispatch(load_spec_spells(spec_slug))
        })
    }, [specs])

    // useEffect(() => {
    // }, [report_id, fight_ids, player_ids])
    // useEffect(() => { dispatch(ui_store.set_boss_slug(boss_slug)) }, [boss_slug])
    // useEffect(() => { dispatch(ui_store.set_spec_slug(spec_slug)) }, [spec_slug])

    // useEffect(() => {
    //     if (!spec) { return }
    //     if (spec.loaded) { return } // skip if we already have them
    //     dispatch(load_spec_spells(spec.full_name_slug))
    // }, [spec])

    // useEffect(() => {
    //     if (!boss) { return }
    //     if (boss.loaded) { return } // skip if we already have them
    //     dispatch(load_boss_spells(boss.full_name_slug))
    // }, [boss])

    // load fights
    // useEffect(() => {
    //     dispatch(load_report_fights(report_id, search)) // [fight_id], [player_id]))
    // }, [report_id, fight_id, player_id])


    ////////////////////////////////////////////////////////////////////////////
    // Render
    //
    return (
        <div className={mode}>

            <div className="mt-3 flex-row d-flex flex-wrap-reverse">
                <ReportHeader />
                <ReportNavbar />
            </div>

             <div className={`${is_loading ? "loading_trans" : ""}`}>
                <ReportSettingsBar />
            </div>
            {is_loading && <LoadingOverlay />}

            <div className={`p-2 bg-dark rounded border d-flex ${is_loading ? "loading_trans" : ""}`}>
                <PlayerNamesList />
                <TimelineCanvas />
            </div>
        </div>
    );
}
