
import { useSelector } from 'react-redux'

import NavbarSpecGroup from "./NavbarSpecGroup.jsx"
import { MODES } from '../../store/ui.js'
import NavbarBossGroup from './NavbarBossGroup.jsx'


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
