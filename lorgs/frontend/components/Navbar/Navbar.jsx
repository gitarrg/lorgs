
import React from 'react'
import { useSelector } from 'react-redux'

import NavbarBossButton from "./NavbarBossButton.jsx"
import NavbarSpecGroup from "./NavbarSpecGroup.jsx"
import { MODES } from '../../store/ui.js'
import { get_bosses } from '../../store/bosses.js'


////////////////////////////////////////////////////////////////////////////////


function NavbarGroup({children, className}) {

    if (!children) return null
    return (
        <div className={`navbar_group p-1 bg-dark border rounded ${className}`}>
            {children}
        </div>
    )
}

function NavbarBossGroup({ }) {
    const bosses = useSelector(state => get_bosses(state))

    return (
        <NavbarGroup className = "navbar_boss">
            {Object.values(bosses).map(boss =>
                <NavbarBossButton key={boss.full_name_slug} boss={boss} />
            )}
        </NavbarGroup>
    )
}


////////////////////////////////////////////////////////////////////////////////


export default function Navbar() {

    const mode = useSelector(state => state.ui.mode)

    return (
        <div className="ml-auto">
            <div className="navbar_container">

                { mode == MODES.SPEC_RANKING && (
                    <NavbarGroup>
                        <NavbarSpecGroup />
                    </NavbarGroup>
                )}

                <NavbarBossGroup />
            </div>
        </div>
    )
}
