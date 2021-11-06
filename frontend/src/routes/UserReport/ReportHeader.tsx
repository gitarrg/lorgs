import HeaderLogo from '../../components/HeaderLogo';
import { useAppSelector } from '../../store/store_hooks';
import { get_report_id } from '../../store/user_reports';

export default function ReportHeader() {

    // Hooks
    const report_id = useAppSelector(state => get_report_id(state))

    /////////////////
    // Render
    return (
        <h1 className="m-0 d-flex align-items-center">
            <HeaderLogo />
            <span className="wow-boss ml-2">Report: {report_id}</span>
        </h1>
    )
}
