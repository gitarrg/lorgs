import { useEffect } from "react";
import { useForm, FormProvider } from "react-hook-form";

import FightSelectList from "./FightSelectList";
import FormGroup from "./FormGroup";
import HeaderLogo from "../../components/HeaderLogo";
import PlayerSelectList from "./PlayerSelectList";
import UrlInput from "./UrlInput";
import { load_report } from "../../store/user_reports";
import { useAppDispatch, useAppSelector } from '../../store/store_hooks'

// @ts-ignore
import styles from "./UserReportIndex.scss"


export default function UserReportIndex() {

    const dispatch = useAppDispatch()

    ////////////////////////////////
    // Hooks
    //
    const form_methods  = useForm({mode: "onChange"});
    // for dev only
    useEffect(() => {
        let report_code = "QKh6q8f2dDAXrTw1"
        report_code = "j68Fkv7DaVfmWbrc"
        form_methods.setValue("report_url", `https://www.warcraftlogs.com/reports/${report_code}`)
        dispatch(load_report(report_code))
    }, [])


    ////////////////////////////////
    // Callbacks
    //
    function submit(form_data) {
        console.log("submitting the form!", form_data)
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

                <div className="d-flex gap-2">
                    {/* Fight Selection */}
                    <FormGroup title="Fights:">
                        <FightSelectList />
                    </FormGroup>

                    {/* Player Selection */}
                    <FormGroup title="Players:">
                        <PlayerSelectList />
                    </FormGroup >
                </div>

                <div className="p-2 mt-3">
                    <input type="submit" />
                </div>

            </form>
            </FormProvider>
        </div>
    )
}
