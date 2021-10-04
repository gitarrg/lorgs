
import React from 'react'
import { useSelector } from 'react-redux'

import { MODES } from "../../data_store.js"

import NavbarBossButton from "./NavbarBossButton.jsx"
import NavbarSpecGroup from "./NavbarSpecGroup.jsx"


////////////////////////////////////////////////////////////////////////////////

function HomeButton() {
    /* regular link for now */
    return (
        <a href="/" title="home" data-tip="back to start page">
            <i className="fas fa-home fa-2x"/>
        </a>
    )
}


////////////////////////////////////////////////////////////////////////////////


function NavbarGroup({children}) {
    
    if (!children) return null

    
    return (
        <div className="navbar_group p-1 bg-dark border rounded">
            {children}
        </div>
    )
}


////////////////////////////////////////////////////////////////////////////////


export default function Navbar() {

    const bosses = useSelector(state => state.bosses)
    const mode = useSelector(state => state.mode)

    return (
        <div className="ml-auto">
            <div className="navbar_container">


                { mode == MODES.SPEC_RANKING && (
                    <NavbarGroup>
                        <NavbarSpecGroup />
                    </NavbarGroup>
                )}

                <NavbarGroup>
                    {bosses.map(boss =>
                        <NavbarBossButton key={boss.full_name_slug} boss={boss} />
                    )}
                </NavbarGroup>

                <NavbarGroup>
                    <HomeButton />
                </NavbarGroup>
            </div>
        </div>
    )
}
