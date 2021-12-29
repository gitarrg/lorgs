import FaButton from './shared/FaButton'
import Icon from '../shared/Icon'
import { ControlledMenu, MenuItem, MenuState, SubMenu, applyStatics } from '@szhsin/react-menu';
import { get_class, get_class_names } from '../../store/classes'
import { get_spec } from '../../store/specs';
import { set_filter } from '../../store/ui';
import { useAppDispatch, useAppSelector } from '../../store/store_hooks'
import { useRef, useState } from 'react'


/**
 * Menu Item for toggle a individual spec
 */
function SpecOption({spec_name, ...props} : {spec_name : string} ) {

    const value = useAppSelector(state => state.ui.filters.spec[spec_name]) ?? true // undefined -> show
    const dispatch = useAppDispatch()
    const spec = useAppSelector(state => get_spec(state, spec_name))
    if (!spec) { return null}

    function onClick() {
        dispatch(set_filter({ group: "spec", name: spec_name, value: !value}))
    }

    return (
        <MenuItem {...props} type="checkbox" checked={!value} onClick={onClick}>
            <Icon spec={spec} size="s" />
            <span className={`ml-1 wow-${spec.class.name_slug}`}>{spec.name}</span>
        </MenuItem>
    )
}
applyStatics(MenuItem)(SpecOption)


function ClassOption({class_name, ...props} : {class_name : string} ) {

    const wow_class = useAppSelector(state => get_class(state, class_name))
    if (class_name === "other") { return null }
    if (!wow_class) { return null}

    return (
        <SubMenu
            {...props}
            label={
                <>
                    <Icon spec={wow_class} size="s" />
                    <span className={`ml-1 wow-${wow_class.name_slug}`}>{wow_class.name}</span>
                </>
            }
        >
            {wow_class.specs.map(name => <SpecOption key={name} spec_name={name} />)}
        </SubMenu>
    )
}
applyStatics(SubMenu)(ClassOption) // flag it as a submenu


export default function FilterDropdownButton() {


    const ref = useRef(null);
    const [state, setState] = useState<MenuState>("closed");

   const class_names = useAppSelector(get_class_names)

    return <>

            <div ref={ref} onMouseEnter={() => setState('open')}>
                <FaButton icon_name="fas fa-user"/>
            </div>
            
            <ControlledMenu
                state={state} anchorRef={ref}
                onMouseLeave={() => setState('closed')}
                submenuCloseDelay={0} submenuOpenDelay={0}
            >
                {class_names.map(name => <ClassOption key={name} class_name={name} />)}
            </ControlledMenu>
    </>
}

