import { useEffect } from "react";
import { useForm, FormProvider } from "react-hook-form";
import FightSelectList from "./FightSelectList";
import FormGroup from "./FormGroup";
import HeaderLogo from "../../components/HeaderLogo";
import LoadingOverlay from "../../components/shared/LoadingOverlay";
import PlayerSelectList from "./PlayerSelectList";
import UrlInput from "./UrlInput";
import { build_url_search_string, get_is_loading, load_report, load_report_overview } from "../../store/user_reports";
import { useAppDispatch, useAppSelector } from '../../store/store_hooks'
import { useHistory } from "react-router";

// @ts-ignore
import styles from "./UserReportIndex.scss"


/** input: [undefined, undefined, true, undefine]
 * step 1: extract indicies (put null where it was undefined)
 * step 2: filter out only the indicies that are non null
 */
function filter_form_select(values: [boolean|undefined]) {
    return values?.map((v, i) => v ? i : null).filter(i => i !== null)
}


export default function UserReportIndex() {

    const dispatch = useAppDispatch()
    let history = useHistory();

    ////////////////////////////////
    // Hooks
    //
    const is_loading = useAppSelector(state => get_is_loading(state))

    const form_methods  = useForm({mode: "onChange"});
    let selected_players = form_methods.watch("players") || []
    let selected_fights = form_methods.watch("fights") || []

    selected_players = filter_form_select(selected_players)
    selected_fights = filter_form_select(selected_fights)
    const enabled = selected_players?.length && selected_fights?.length

    // for dev only
    useEffect(() => {
        let report_code = "QKh6q8f2dDAXrTw1"
        report_code = "j68Fkv7DaVfmWbrc"
        form_methods.setValue("report_url", `https://www.warcraftlogs.com/reports/${report_code}`)
        dispatch(load_report_overview(report_code))
    }, [])


    ////////////////////////////////
    // Callbacks
    //
    async function submit(form_data) {
        const report_id = form_methods.getValues("report_code")


        const search = build_url_search_string({fight_ids: selected_fights, player_ids: selected_players})
        const response = await dispatch(load_report(report_id, selected_fights, selected_players))

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
        history.push(url)
    }


    ////////////////////////////////
    // Render
    //
    return (
        <div className="d-flex justify-content-center">

            <FormProvider {...form_methods}>
            <form onSubmit={form_methods.handleSubmit(submit)} className={`${styles.container} mt-5`}>

                {/* Header */}
                <h2 className="m-0 gap-2 d-flex align-items-center wow-artifact">
                    <HeaderLogo wow_class="wow-artifact" />
                    <span>Load Report:</span>
                </h2>

                {/* URL Input */}
                <FormGroup title="Report URL:">
                    <UrlInput />
                </FormGroup>

                {is_loading && <LoadingOverlay />}

                <div className={`d-flex gap-2 ${is_loading ? "loading_trans" : ""} `}>
                    {/* Fight Selection */}
                    <FormGroup title="Fights:">
                        <FightSelectList />
                    </FormGroup>

                    {/* Player Selection */}
                    <FormGroup title="Players:">
                        <PlayerSelectList />
                    </FormGroup >
                </div>

                <div className="mt-3 ml-auto">
                    <button
                        className={`${styles.submit_button} button grow-when-touched`}
                        disabled={!enabled}
                        type="submit">
                            Load
                    </button>
                </div>

            </form>
            </FormProvider>
        </div>
    )
}
