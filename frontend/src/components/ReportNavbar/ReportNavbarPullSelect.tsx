import { useAppSelector } from '../../store/store_hooks'
import { get_selected_fights } from '../../store/user_reports'

// @ts-ignore
import styles from "./ReportNavbar.scss"


function build_label(selected_fights: number[]) {
    const n = selected_fights.length
    if (n === 0) { return "select some pulls"}

    const pulls = [...selected_fights].sort((a, b) => a < b ? -1 : 1).join(", ")
    return `Pull${n > 1 ? "s": ""}: ${pulls}`
}


export default function ReportNavbarPullSelect({onClick} : {onClick: Function}) {

    const selected_fights = useAppSelector(state => get_selected_fights(state))
    const label = build_label(selected_fights)

    // Render
    return <h3
        className={styles.group_header}
        onClick={onClick}>{label}
    </h3>
}
