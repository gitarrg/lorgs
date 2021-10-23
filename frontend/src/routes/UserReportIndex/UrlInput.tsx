import { KeyboardEvent } from 'react'
import { load_report_overview, get_is_loading } from "../../store/user_reports";
import { useAppDispatch, useAppSelector } from '../../store/store_hooks'
import { useFormContext, useWatch } from 'react-hook-form';
// @ts-ignore
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
function report_code_from_url(url="") {
    if (!url) { return ""}

    const match = url.match(URL_REGEX);
    if (!match) { return "" }

    return match.groups.code ?? ""
}


/** an URL-Input Field and Button to load the URL
 *
 */
export default function UrlInput({input_name="report_url"}) {

    ////////////////////////////////
    // Hooks
    const dispatch = useAppDispatch()
    const is_loading = useAppSelector(state => get_is_loading(state))
    const { register, setValue, formState: { errors } } = useFormContext();
    const url = useWatch({name: input_name})


    ////////////////////////////////
    // Vars
    const report_code = report_code_from_url(url)
    const is_valid = report_code != ""
    const valid_css = is_valid ? "valid" : "invalid"


    ////////////////////////////////
    // Handlers

    /** Update the stored report code */
    function onClick() {
        setValue("report_code", report_code)
        dispatch(load_report_overview(report_code))
    }

    /** Allow users to submit their URL by pressing enter */
    function onKeyDown(event: KeyboardEvent<HTMLInputElement>) {
        if (event.key == "Enter") { onClick() }
    }

    ////////////////////////////////
    // Render
    return (

        <div className="bg-dark rounded p-2">
            <div className={`${styles.url_input} input-group`}>

                {/* Input */}
                <input
                    {...register(input_name, {
                        validate: () => is_valid || "invalid url",
                    })}
                    type="text"
                    onKeyDown={onKeyDown}
                    className={`form-input form-control ${valid_css}`}
                    placeholder={PLACEHOLDER}
                />

                {/* Button */}
                <button
                    type="button"
                    className="button"
                    disabled={!is_valid || is_loading}
                    onClick={onClick}>
                    load ▶
                </button>

            </div>

            {/* Error Messages */}
            {url && !is_valid &&  (
                <span className="text-danger mt-1 small">
                    {errors[input_name]?.message}
                </span>
            )}
        </div>
    )
}
