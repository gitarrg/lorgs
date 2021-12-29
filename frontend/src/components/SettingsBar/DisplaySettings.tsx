import ButtonGroup from './shared/ButtonGroup'
import FaButton from './shared/FaButton'
import ClassSpecFilterMenu from "./ClassSpecFilterMenu"
import { ControlledMenu, MenuItem, applyStatics, MenuState } from '@szhsin/react-menu';
import { update_settings } from '../../store/ui'
import { useAppSelector } from '../../store/store_hooks'
import { ReactNode, useRef, useState } from 'react'
import { useDispatch } from 'react-redux'


function DisplayToggleItem({attr_name, children, ...props} : {attr_name : string, children : ReactNode}) {

    const value = useAppSelector(state => state.ui.settings[attr_name])
    const dispatch = useDispatch()

    function onClick() {
        dispatch(update_settings({[attr_name]: !value}))
    }

    return (
        <MenuItem type="checkbox" checked={value} onClick={onClick} {...props}>
            {children}
        </MenuItem>
    )
}
applyStatics(MenuItem)(DisplayToggleItem)


function SettingsDropdown() {

    const ref = useRef(null);
    const [state, setState] = useState<MenuState>("closed");

    return <>
        <div ref={ref} onMouseEnter={() => setState('open')}>
            <FaButton icon_name="fas fa-cog"/>
        </div>

        <ControlledMenu
            state={state} anchorRef={ref}
            onMouseLeave={() => setState('closed')}
            submenuCloseDelay={0} submenuOpenDelay={0}
        >

            <DisplayToggleItem attr_name="show_cooldown"><i className="fas fa-image mr-1"/>show cooldown durations</DisplayToggleItem>
            <DisplayToggleItem attr_name="show_casticon"><i className="fas fa-clock mr-1"/>show spell icons</DisplayToggleItem>
            <DisplayToggleItem attr_name="show_casttime"><i className="fas fa-stream mr-1"/>show cast time</DisplayToggleItem>
            <DisplayToggleItem attr_name="show_duration"><i className="fas fa-hourglass mr-1"/>show active duration</DisplayToggleItem>
        </ControlledMenu>
    </>
}



export default function DisplaySettings() {

    return (
        <>
            <ButtonGroup name="Display" side="left">
                <SettingsDropdown />
                <ClassSpecFilterMenu />
            </ButtonGroup>
        </>
    )
}
