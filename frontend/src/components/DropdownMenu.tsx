import { ControlledMenu, useMenuState } from '@szhsin/react-menu';
import { ReactNode, useRef } from 'react'


export default function DropdownMenu({button, children} : {button: ReactNode, children: ReactNode}) {

    const ref = useRef(null);
    const { toggleMenu, ...menuProps } = useMenuState();

    const callbacks = {
        onMouseEnter: () => toggleMenu(true),
        onMouseLeave: () => toggleMenu(false),
        onClose: () => toggleMenu(false),
    }

    return (
        <div> {/* wrapper to avoid issues if the parent uses grid-gap */}

            {/* Button */}
            <div {...callbacks} ref={ref} className="active">
                {button}
            </div>

            {/* Menu Content */}
            <ControlledMenu {...callbacks} {...menuProps} anchorRef={ref}>
                {children}
            </ControlledMenu>
        </div>
    )
}