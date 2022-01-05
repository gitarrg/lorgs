import { KeyboardEvent, useEffect } from 'react'
import { load_report_overview, get_is_loading, get_user_report } from "../../store/user_reports";
import { useAppDispatch, useAppSelector } from '../../store/store_hooks'
import { useFormContext, useWatch } from 'react-hook-form';
import { useLocation } from 'react-router';
import styles from "./UrlInput.scss"


/** text to show when the URL input is empty */
const PLACEHOLDER = "https://www.warcraftlogs.com/reports/<report code>"


/** regex to match urls from warcraftlogs */
const URL_REGEX = RegExp(
    ""
    + /warcraftlogs\.com/.source   //  domain
    + /\/reports/.source           //  /reports
    + /\/(?<code>\w{16})/.source   //  /report-code
, "i")


/** Extract the report code from an url. */
function report_id_from_url(url="") {
    if (!url) { return ""}

    const match = url.match(URL_REGEX);
    if (!match) { return "" }

    return match.groups?.code ?? ""
}


/** an URL-Input Field and Button to load the URL
 *
 */
export default function UrlInput({input_name="report_url"}) {

    ////////////////////////////////
    // Hooks: Redux
    const dispatch = useAppDispatch()
    const is_loading = useAppSelector(state => get_is_loading(state))
    const user_report = useAppSelector(get_user_report)
    // Hooks: Router
    const { search } = useLocation();
    // Hooks: Form
    const { register, setValue, formState: { errors } } = useFormContext();
    const url = useWatch({name: input_name})


    ////////////////////////////////
    // Vars
    const report_id = report_id_from_url(url)
    const is_valid = report_id != "" && user_report.error == ""

    ////////////////////////////////
    // Handlers
    useEffect(() => {
        const search_params = new URLSearchParams(search)
        const report_id = search_params.get("report_id")
        if (!report_id) { return }
        setValue("report_url", `https://www.warcraftlogs.com/reports/${report_id}`)

        setValue("report_code", report_id)
        dispatch(load_report_overview(report_id))
    }, [search])


    /** Update the stored report code */
    function onClick() {
        setValue("report_code", report_id)
        dispatch(load_report_overview(report_id, false))
    }

    function onClickReload() {
        dispatch(load_report_overview(report_id, true))
    }


    /** Allow users to submit their URL by pressing enter */
    function onKeyDown(event: KeyboardEvent<HTMLInputElement>) {
        if (event.key == "Enter") {
            event.preventDefault()
            onClick()
        }
    }


    ////////////////////////////////
    // Render
    return (
        <div>
            <div className={`${styles.url_input} bg-dark rounded p-2 input-group`}>

                {/* Input */}
                <input
                    {...register(input_name, {
                        validate: () => is_valid || "invalid url",
                    })}
                    type="text"
                    onKeyDown={onKeyDown}
                    className={`form-input form-control ${is_valid ? "valid" : "invalid"}`}
                    placeholder={PLACEHOLDER}
                />

                {/* Button: Load */}
                <button
                    type="button"
                    className="button"
                    disabled={!is_valid || is_loading}
                    data-tooltip="Load Report"
                    onClick={onClick}>
                        <i className="fas fa-chevron-right"></i>
                </button>

                {/* Button: Reload */}
                <button
                    type="button"
                    className="button"
                    disabled={!is_valid || is_loading}
                    data-tooltip="Reload"
                    onClick={onClickReload}>
                        <i className="fas fa-sync-alt"></i>
                </button>

            </div>

            {/* Error Messages */}
            {url && !is_valid &&  (
                <span className="text-danger mt-1">
                    {errors[input_name]?.message}
                    {user_report.error ?? ""}
                </span>
            )}
        </div>
    )
}
