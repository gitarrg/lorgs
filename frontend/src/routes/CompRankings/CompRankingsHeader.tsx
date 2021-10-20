import { useLocation } from 'react-router-dom';

import CompPreview, { CompCountMap } from "../../components/CompPreview"
import HeaderLogo from '../../components/HeaderLogo';
import { get_boss } from '../../store/bosses';
import { useAppSelector } from '../../store/store_hooks';



function parse_comp_search_string(search: string) {

    const result: { [key: string]: CompCountMap} = {}
    const params = new URLSearchParams(search)
    for(let [group, value] of params.entries()) {
        group = `${group}s` // pluralize "role" --> "roles"
        let [key, op, count] = value.split(".") // assume "tank.eq.2"

        // append to result
        result[group] = result[group] || {}
        result[group][key] = {op, count}
    }
    return result
}


export default function CompRankingsHeader() {

    // Hooks
    const boss = useAppSelector(state => get_boss(state))
    const { search } = useLocation();
    if (!boss) { return null }

    const comp_info = parse_comp_search_string(search)
    const comp_preview = <CompPreview {...comp_info} placeholder="any comp"/>

    /////////////////
    // Render
    return (
        <h1 className="m-0 d-flex align-items-center">
            <HeaderLogo />
            <span className="wow-boss ml-2">{boss.full_name}</span>
            <span>&nbsp;vs.&nbsp;</span>
            {comp_preview}
        </h1>
    )
}


