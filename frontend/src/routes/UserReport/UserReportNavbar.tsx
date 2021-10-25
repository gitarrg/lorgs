import { Link } from 'react-router-dom'
import { useAppSelector } from '../../store/store_hooks'
import { get_report_id } from '../../store/user_reports'

// @ts-ignore
import styles from "./UserReportNavbar.scss"


export default function UserReportNavbar() {


    const report_id = useAppSelector(get_report_id)
    const url = `/user_report?report_id=${report_id}`

    // Render
    return (
        <Link to={url}>
            <button className={`${styles.button} button grow-when-touched`} >
                <span>Select different Pulls/Players</span>
            </button>
        </Link>
    )
}
