import Icon from '../../components/shared/Icon'
import IndexModuleLink from "./IndexModuleLink"
import { get_boss } from "../../store/bosses"
import { get_player_roles } from '../../store/roles'
import { useAppSelector } from "../../store/store_hooks"


// default boss name to show here
const BOSS_NAME = "sylvanas-windrunner"


function RolesList() {

    const roles = useAppSelector(get_player_roles)

    return (
        <>
        {roles.map(role =>
            <Icon key={role.code} spec={role} size="l" />
        )}
        </>
    )
}


export default function IndexCompsGroup() {

    const boss = useAppSelector(state => get_boss(state, BOSS_NAME))
    if (!boss) { return null }

    // Render
    return (
        <IndexModuleLink title="Top Reports by Comp:" url="/comp_ranking/search">
            <Icon spec={boss} size="l" />
            <span className="h2"> vs. </span>
            <RolesList />
        </IndexModuleLink>
    )
}

