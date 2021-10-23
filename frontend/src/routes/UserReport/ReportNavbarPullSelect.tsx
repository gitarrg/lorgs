import { useAppSelector } from '../../store/store_hooks'
import { get_user_report_fights } from '../../store/user_reports'
import type Fight from '../../types/fight'

import styles from "./ReportNavbar.scss"

function FightRow({fight} : {fight: Fight}) {

    return (
        <div>
            <span>Pull: {fight.fight_id}</span>

        </div>

    )

}


export default function ReportNavbarPullSelect() {


    const fights = useAppSelector(state => get_user_report_fights(state))

    const current_pull = "12"

    return (
        <div className={`${styles.dropdown_container} bg-dark border p-2 rounded`}>

            <span>Pull: {current_pull}</span>

            <div className={styles.dropdown_container__dropdown}>
                <div className="bg-dark p-2 rounded border">
                {fights.map(fight =>
                    <FightRow key={fight.fight_id} fight={fight} />
                )}
                </div>
            </div>
        </div>
    )
}
