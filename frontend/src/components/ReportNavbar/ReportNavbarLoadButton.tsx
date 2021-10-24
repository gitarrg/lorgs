import { build_url_search_string, get_report_id, get_search_string, load_report, report_requires_reload } from '../../store/user_reports';
import { get_fight_ids, get_all_fights } from '../../store/fights';
import { useAppDispatch, useAppSelector } from '../../store/store_hooks';
import { useHistory } from 'react-router';

// @ts-ignore
import styles from "./ReportNavbar.scss";


export function ReportNavbarLoadButton() {


    ////////////////////////////////
    // Hooks
    //
    const history = useHistory();
    const dispatch = useAppDispatch()
    const current_fight_ids = useAppSelector(state => get_fight_ids(state))
    const current_fights = useAppSelector(state => get_all_fights(state))
    const report_id = useAppSelector(state => get_report_id(state))

    // todo: only call inside callback
    const new_search = useAppSelector(state => get_search_string(state))
    const requires_reload = useAppSelector(state => report_requires_reload(state))

    ////////////////////////////////
    // Callbacks
    //
    async function onClick() {

        history.push({search: new_search});
        return

        const player_ids = [...context.selected_players]

        // check if we need to load anything
        // only need to know if there is anything
        const needs_to_load = fight_ids.some(fight_id => {

            const fight = current_fights[fight_id]

            // the fight itself needs to be loaded
            if (!fight) { return true }

            // wtb normalised data
            const fight_player_ids = fight.players.map(player => player.source_id)
            const missing_players = player_ids.filter(player_id => !fight_player_ids.includes(player_id))

            // need to load due to missing player
            if (missing_players.length > 0 ) { return true }
        });

        // dispatch(report_selection_changed({fight_ids, player_ids}))
        const search = build_url_search_string({ player_ids, fight_ids });
        console.log({search});

        // if no load is required.. we can simply update the URL
        history.push({search: new_search});
        if (!needs_to_load) {
            history.push({search: search});
        }

        const response = await dispatch(load_report(report_id, fight_ids, player_ids))

        // Redirect to the next page.
        // if we get a task id, we go via the loading page
        let url
        if (response.task_id) {
            url = `/user_report/load?task=${response.task_id}&report_id=${report_id}&${search}`
        }
        // otherwise we can go directly to the report page
        else {
            url = `/user_report/${report_id}?${search}`
        }
        return history.push(url)
    }


    ////////////////////////////////
    // Render
    //
    return (
        <button
            className={`${styles.submit_button} button grow-when-touched`}
            onClick={onClick}
            disabled={!requires_reload}
        >
            <span>Load</span>
        </button>
    );

}
