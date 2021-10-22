import { useEffect } from "react";
import { useForm, FormProvider } from "react-hook-form";

import FormGroup from "./FormGroup";
import HeaderLogo from "../../components/HeaderLogo";
import UrlInput from "./UrlInput";
import styles from "./UserReportIndex.scss"



export default function UserReportIndex() {

    ////////////////////////////////
    // Hooks
    //
    const form_methods  = useForm({mode: "onChange"});
    // for dev only
    useEffect(() => {
        form_methods.setValue("report_url", "https://www.warcraftlogs.com/reports/j68Fkv7DaVfmWbrc")
    }, [])


    ////////////////////////////////
    // Callbacks
    //
    function submit(form_data) {
        console.log("submit!", form_data)
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

                <div className="p-2 mt-3">
                    <input type="submit" />
                </div>

            </form>
            </FormProvider>
        </div>
    )
}
