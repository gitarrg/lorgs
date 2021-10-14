/*
    Component to show the currently selected Boss
*/

import { useWatch } from "react-hook-form";
import { get_boss } from '../../store/bosses';
import { useAppSelector } from '../../store/store_hooks';


export default function BossSelection() {

    // currently selected boss name
    const boss_name_slug = useWatch({name: "boss_name_slug"})
    const boss = useAppSelector(state => get_boss(state, boss_name_slug))

    const have_boss = boss && boss.full_name
    const header_content = have_boss ? <span className="wow-boss">{boss.full_name}</span> : <div className="text-muted">select a boss</div>

    return (
        <>
            <h1 className="">{header_content}</h1>
            {have_boss && <img className="icon-l rounded shadow wow-border-boss ml-2" src={boss.icon_path} alt={boss.name}></img>}
        </>
    )
}
