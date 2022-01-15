import HeaderLogo from '../../components/HeaderLogo';
import { useAppSelector } from '../../store/store_hooks';
import { get_user_report } from '../../store/user_reports';

export default function ReportHeader() {

    // Hooks
    const report = useAppSelector(get_user_report)

    const date = new Date(report.date * 1000)
    const date_str = date.toLocaleDateString()  // ref: https://www.freecodecamp.org/news/how-to-format-dates-in-javascript/
    const date_str_full = date.toLocaleString()

    const author_name = report.guild || ("Lorrger: " + report.owner)

    /////////////////
    // Render
    return (
        <h1 className="m-0 d-flex align-items-center">
            <HeaderLogo wow_class='wow-artifact' />
            <span className="wow-artifact ml-2">Custom Report:</span>
            <span className="" data-tooltip={date_str_full} data-tooltip-dir="down">&nbsp;{date_str} - {author_name}</span>
        </h1>
    )
}
