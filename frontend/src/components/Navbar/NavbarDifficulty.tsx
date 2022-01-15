import { applyStatics, ControlledMenu, MenuItem, MenuState } from '@szhsin/react-menu';
import { useEffect, useRef, useState } from 'react'
import { get_difficulty, get_mode } from '../../store/ui';
import NavbarGroup from './NavbarGroup';

import styles from "./NavbarDifficulty.scss"
import { useAppSelector } from '../../store/store_hooks';
import { NavLink } from 'react-router-dom';
import WebpImg from '../WebpImg';
import Icon from '../shared/Icon';


const DIFFICULTY_COLOR = {
    mythic: "wow-epic",
    heroic: "wow-rare",
}


function DifficultyIcon({difficulty} : {difficulty : string}) {

    const class_name = DIFFICULTY_COLOR[difficulty] || ""

    const label = difficulty[0].toUpperCase()
    return <span className={`${styles.icon} ${class_name} icon-m shadow`}>{label}</span>

}


function NavbarDifficultyOption({difficulty, className, ...props} : {difficulty: string, className: string}) {

    const mode = useAppSelector(get_mode);
    const boss_slug : string = useAppSelector(state => state.ui.boss_slug);
    const spec_slug = useAppSelector(state => state.ui.spec_slug);

    difficulty = difficulty.toLowerCase()
    const link = `/${mode}/${spec_slug}/${boss_slug}/${difficulty}`;
    const class_name = DIFFICULTY_COLOR[difficulty] || ""

    return (
        <NavLink to={link} className={`${className} ${styles.option}`} activeClassName="active">
            <MenuItem {...props}>
                <DifficultyIcon difficulty={difficulty}/>
                <span className={`${class_name} ml-1`}>{difficulty}</span>
            </MenuItem>
        </NavLink>
    )
}
applyStatics(MenuItem)(NavbarDifficultyOption)


export default function NavbarDifficulty() {

    const ref = useRef(null);
    const [state, setState] = useState<MenuState>("closed");

    // const [difficulty, setDifficulty] = useState("mythic");
    const difficulty = useAppSelector(get_difficulty)


    useEffect(() => setState("open"), [])



    return (
        <NavbarGroup>

            <div ref={ref} onMouseEnter={() => setState('open')} className="active">
                <DifficultyIcon difficulty={difficulty}/>
            </div>

            <ControlledMenu
                state={state} anchorRef={ref}
                onMouseLeave={() => setState('closed')}
                submenuCloseDelay={10} submenuOpenDelay={0}
            >
                <NavbarDifficultyOption difficulty="mythic" className="wow-epic" />
                <NavbarDifficultyOption difficulty="heroic" className="wow-rare" />
            </ControlledMenu>
        </NavbarGroup>
    )
}


