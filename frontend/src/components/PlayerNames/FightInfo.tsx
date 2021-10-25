import Fight from "../../types/fight";
import { useAppSelector } from '../../store/store_hooks';
import { get_mode, MODES } from "../../store/ui";

import style from "./FightInfo.scss"


export function FightInfo({ fight }: { fight: Fight; }) {

    const mode = useAppSelector(get_mode)
    if (mode != MODES.USER_REPORT ) { return null }

    // Render
    return (
        <div className={style.container}>
            #{fight.fight_id}

        </div>
    );

}
