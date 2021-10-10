/*
    Component to show the currently selected Roles/Specs
*/

import React from 'react'
import { useWatch } from "react-hook-form";
import CompPreview from '../../components/CompPreview.jsx';



export default function PlayerSelection() {

    // Fetch Form Vars
    const roles = useWatch({name: "role"})
    const specs = useWatch({name: "spec"})

    // Build Content
    let header_content = <CompPreview roles={roles} specs={specs} placeholder="any comp"/>
    return <h1 className="m-0 mr-auto">{header_content}</h1>
}
