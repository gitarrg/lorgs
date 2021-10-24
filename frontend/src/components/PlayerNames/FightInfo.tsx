import Fight from "../../types/fight";

import style from "./FightInfo.scss"


export function FightInfo({ fight }: { fight: Fight; }) {


    return (
        <div className={style.container}>
            #{fight.fight_id}

        </div>
    );

}
