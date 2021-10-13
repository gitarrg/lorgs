
import { useSelector } from 'react-redux'

import NavbarBossGroup from './NavbarBossGroup'
import NavbarSpecGroup from "./NavbarSpecGroup"
import { MODES } from '../../store/ui'


////////////////////////////////////////////////////////////////////////////////

export default function Navbar() {

    const mode: string = useSelector(state => state.ui.mode)

    return (
        <div className="ml-auto">
            <div className="navbar_container">
                { mode == MODES.SPEC_RANKING && <NavbarSpecGroup /> }
                <NavbarBossGroup />
            </div>
        </div>
    )
}
