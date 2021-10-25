import FightSelectGrid from "../../components/ReportNavbar/FightSelectList"
import FormGroup from "./FormGroup"
import HeaderLogo from "../../components/HeaderLogo"
import LoadingOverlay from "../../components/shared/LoadingOverlay"
import PlayerSelectGrid from "../../components/ReportNavbar/PlayerSelectList"
import UrlInput from "./UrlInput"
import { SubmitButton } from "./SubmitButton";
import { get_is_loading } from "../../store/user_reports"
import { useAppSelector } from "../../store/store_hooks"
import { useForm, FormProvider } from "react-hook-form";

// @ts-ignore
import styles from "./UserReportIndex.scss"


/** input: [undefined, undefined, true, undefine]
 * step 1: extract indicies (put null where it was undefined)
 * step 2: filter out only the indicies that are non null
 */
export function filter_form_select(values: [boolean|undefined]) {
    return values?.map((v, i) => v ? i : null).filter(i => i !== null)
}


export default function UserReportIndex() {

    ////////////////////////////////
    // Hooks
    //
    const is_loading = useAppSelector(get_is_loading)
    const form_methods  = useForm();

    ////////////////////////////////
    // Render
    //
    return (
        <div className="d-flex justify-content-center">

            <FormProvider {...form_methods}>
            <form className={`${styles.container} mt-5`}>

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
                        <FightSelectGrid />
                    </FormGroup>

                    {/* Player Selection */}
                    <FormGroup title="Players:">
                        <PlayerSelectGrid />
                    </FormGroup >
                </div>

                <div className="mt-3 ml-auto">
                    <SubmitButton />
                </div>

            </form>
            </FormProvider>
        </div>
    )
}
