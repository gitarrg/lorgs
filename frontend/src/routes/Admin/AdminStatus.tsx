import { Fragment, useEffect, useState } from "react"
import { fetch_data } from "../../api"
import Icon from "../../components/shared/Icon"
import { get_bosses } from "../../store/bosses"
import { get_player_roles } from "../../store/roles"
import { get_specs } from "../../store/specs"
import { load_status } from "../../store/status"
import { useAppDispatch, useAppSelector } from "../../store/store_hooks"
import type Boss from "../../types/boss"
import type Role from "../../types/role"
import type Spec from "../../types/spec"

import styles from "./AdminStatus.scss"

import moment from "moment"


function get_age(last_update: moment) {
    const diff = moment().diff(last_update, "days")
    console.log("diff", diff)

    if (diff > 7) { return "week"}
    if (diff > 3) { return "three_days"}
    if (diff > 1) { return "day"}
    { return "fresh"}
}



function StatusCell({spec, boss} : {spec: Spec, boss: Boss}) {

    const status_info = useAppSelector(state => state.status)
    const info = status_info.status?.[spec.full_name_slug]?.[boss.full_name_slug]
    if (!info) { return <td> - </td>}

    const last_update = moment(info.updated * 1000)
    return <td data-age={get_age(last_update)} >{last_update.fromNow(true)}</td>

}


function create_role_group(role: Role, all_specs: Spec[], bosses: Boss[]) {

    const specs = all_specs.filter(spec => spec.role == role.code)
    // console.log("specs2", role.code, all_specs.map(spec => spec.role == role.code))
    console.log("all specs", specs)

    return (
        <Fragment key={role.code}>
            {specs.map(spec =>
                <tr key={spec.full_name_slug}>

                    <td><Icon spec={role} size="s" /></td>
                    <td><Icon spec={spec} size="s" /></td>
                    <td className={`wow-${spec.class.name_slug}`}>{spec.name}</td>

                    {bosses.map(boss =>
                        <StatusCell key={`${spec.full_name_slug}-${boss.full_name_slug}`} spec={spec} boss={boss} />
                    )}

                </tr>
            )}
        </Fragment>
    )
}


export default function AdminStatus() {

    const roles = useAppSelector(state => get_player_roles(state))
    const specs_map = useAppSelector(state => get_specs(state))
    const bosses_map = useAppSelector(state => get_bosses(state))
    const bosses = Object.values(bosses_map)
    const specs = Object.values(specs_map)

    const dispatch = useAppDispatch()
    const status_info = useAppSelector(state => state.status)
    console.log("status_info", status_info)


    useEffect(() => {
        dispatch(load_status())
    }, [])




    // console.log("roles", roles)
    // console.log("specs", specs)
    // console.log("bosses", bosses)


    return (
        <div className="p-2 bg-dark border">
            <table className={styles.status_table}>

                <thead>
                    <tr>
                        <th></th>
                        <th></th>
                        <th></th>
                    {bosses.map(boss =>
                        <th key={boss.full_name_slug} ><Icon spec={boss} size="s"/></th>
                    )}
                        </tr>
                </thead>
                <tbody>
                    {roles.map(role => create_role_group(role, specs, bosses))}
                </tbody>
            </table>
        </div>
    )
}
