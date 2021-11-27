import styles from "./UserReportNavbar.scss"
import { Link } from 'react-router-dom'
import { get_report_id } from '../../store/user_reports'
import { useAppSelector } from '../../store/store_hooks'


export default function UserReportNavbar() {


    const report_id = useAppSelector(get_report_id)
    const url = `/user_report?report_id=${report_id}`

    // Render
    return (
        <Link to={url}>
            <button className={`${styles.button} button grow-when-touched`} >
                <span>Change Selection</span>
            </button>
        </Link>
    )
}
