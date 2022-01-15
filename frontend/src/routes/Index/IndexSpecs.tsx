import { Fragment } from 'react'
import { Link } from 'react-router-dom'
import Icon from '../../components/shared/Icon'
import { get_player_roles } from '../../store/roles'
import { get_spec } from '../../store/specs'
import { useAppSelector } from '../../store/store_hooks'
import type Role from '../../types/role'
import styles from "./IndexSpecs.scss"


const DEFAULT_BOSS = "the-tarragrue"
const DEFAULT_DIFF = "mythic"


function SpecButton({spec_slug=""}) {

    const spec = useAppSelector(state => get_spec(state, spec_slug))
    if (!spec) { return null }

    return (
        <Link to={`/spec_ranking/${spec_slug}/${DEFAULT_BOSS}/${DEFAULT_DIFF}`} data-tooltip={spec.full_name}>
            <Icon spec={spec} alt={spec.full_name} />
        </Link>
    )
}


function create_row(role: Role) {


    return (
        <Fragment key={role.code}>

            {/* Wrapped Icon+Label in one div, to better align the label */}
            <div>
                <Icon spec={role} alt={role.name} />

                <span className={styles.role_name}>
                    {role.name}
                </span>
            </div>

            <div className={styles.spec_button_container}>
                {role.specs.map(spec_slug =>
                    <SpecButton key={spec_slug} spec_slug={spec_slug} />
                )}
            </div>
        </Fragment>

    )
}


export default function IndexSpecs() {

    const roles = useAppSelector(state => get_player_roles(state))

    return (
        <div>
            <h3>Top Parses by Spec:</h3>
            <div className={`${styles.container} bg-dark rounded border p-2`}>
                {roles.map(role => create_row(role))}
            </div>
        </div>
    )
}
