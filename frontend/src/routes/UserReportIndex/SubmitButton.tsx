import { useState } from "react"
import { useFormContext, useWatch } from "react-hook-form";
import { build_url_search_string, load_report } from "../../store/user_reports"
import { useAppDispatch } from '../../store/store_hooks'
import { useHistory } from "react-router"
import { filter_form_select } from "./UserReportIndex";

// @ts-ignore
import styles from "./UserReportIndex.scss";


export function SubmitButton() {

    ////////////////////////////////
    // Hooks
    const [loading, set_loading] = useState(false);

    const dispatch = useAppDispatch();
    let history = useHistory();

    // Form
    const { handleSubmit } = useFormContext();
    const selected_players: Boolean[] = useWatch({ name: "player" });
    const selected_fights: Boolean[] = useWatch({ name: "fight" });


    // enable if at least 1 player and 1 fight is selected
    const enabled = !loading && selected_players?.some(v => v) && selected_fights?.some(v => v);


    ////////////////////////////////
    // Callbacks
    //
    async function submit(form_data) {

        set_loading(true);

        // Get Form Inputs
        const selected_players = filter_form_select(form_data["player"]);
        const selected_fights = filter_form_select(form_data["fight"]);
        const report_id = form_data["report_code"];

        // submit task
        const search = build_url_search_string({ fight_ids: selected_fights, player_ids: selected_players });
        const response = await dispatch(load_report(report_id, selected_fights, selected_players));

        // Redirect to the next page.
        // if we get a task id, we go via the loading page
        if (response.task_id) {
            const url = `/user_report/load?task=${response.task_id}&report_id=${report_id}&${search}`;
            history.push(url);
        }

        // otherwise we can go directly to the report page
        else {
            const url = `/user_report/${report_id}?${search}`;
            history.push(url);
        }
    }

    ////////////////////////////////
    // Render
    return <button
        className={`${styles.submit_button} button grow-when-touched`}
        disabled={!enabled}
        onClick={handleSubmit(submit)}
        type="submit">
        Load
    </button>;
}
