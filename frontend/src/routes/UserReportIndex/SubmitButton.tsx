import { useState } from "react"
import { useFormContext, useWatch } from "react-hook-form";
import { build_url_search_string, get_user_report_fights, load_report } from "../../store/user_reports"
import { useAppDispatch, useAppSelector } from '../../store/store_hooks'
import { useHistory } from "react-router"
import styles from "./UserReportIndex.scss";
import useUser from "../auth/useUser";



/** input: [undefined, undefined, true, undefine]
 * step 1: extract indicies (put null where it was undefined)
 * step 2: filter out only the indicies that are non null
 */
 export function filter_form_select(values: [boolean|undefined]) {

    const indicies = values.map((v, i) => v ? i : -1) // list of: index for selected items & -1 for unselected
    return indicies.filter(i => i >= 0) // only keep selected
}



export function SubmitButton() {

    ////////////////////////////////
    // Hooks
    const [loading, set_loading] = useState(false);

    const dispatch = useAppDispatch();

    let history = useHistory();
    const user = useUser()

    // Form
    const { handleSubmit } = useFormContext();
    const selected_players: Boolean[] = useWatch({ name: "player" });
    const selected_fights: Boolean[] = useWatch({ name: "fight" });

    const fights = useAppSelector(get_user_report_fights)
    if (fights.length == 0) { return null }

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
        const response = await dispatch(load_report(
            report_id,
            selected_fights,
            selected_players,
            user.permissions.includes("user_reports") ? user.id : "",
        ));

        // Redirect to the next page.
        // if we get a task id, we go via the loading page
        if (response.task_id) {
            const url = `/user_report/load?task=${response.task_id}&queue=${response.queue}&report_id=${report_id}&${search}`;
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
