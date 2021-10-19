import Icon from '../../components/shared/Icon'
import { Link } from 'react-router-dom'
import { get_boss } from "../../store/bosses"
import { get_player_roles } from '../../store/roles'
import { useAppSelector } from "../../store/store_hooks"
import styles from "./IndexCompsGroup.scss"


// default boss name to show here
const BOSS_NAME = "sylvanas-windrunner"


export default function IndexCompsGroup() {

    const boss = useAppSelector(state => get_boss(state, BOSS_NAME))
    const roles = useAppSelector(state => get_player_roles(state))
    if (!boss) { return null }

    // Render
    return (
        <div>
            <h3>Top Reports by Comp:</h3>

            <Link to="/comp_ranking/search" className="d-flex">

                <div className={`${styles.container} bg-dark rounded border grow-when-touched p-2 gap-2 d-flex align-items-center`}>

                    <Icon spec={boss} size="l" />
                    <span className="h2"> vs. </span>
                    {roles.map(role =>
                        <Icon key={role.code} spec={role} size="l" />
                    )}
                </div>
            </Link>
        </div>
    )
}

