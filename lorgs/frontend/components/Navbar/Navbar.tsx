
import { useSelector } from 'react-redux'

import NavbarSpecGroup from "./NavbarSpecGroup"
import { MODES } from '../../store/ui'
import NavbarBossGroup from './NavbarBossGroup'


////////////////////////////////////////////////////////////////////////////////

export default function Navbar() {

    const mode = useSelector(state => state.ui.mode)

    return (
        <div className="ml-auto">
            <div className="navbar_container">
                { mode == MODES.SPEC_RANKING && <NavbarSpecGroup /> }
                <NavbarBossGroup />
            </div>
        </div>
    )
}
