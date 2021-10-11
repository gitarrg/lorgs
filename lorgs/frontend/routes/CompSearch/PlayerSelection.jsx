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
    const placeholder = <h1>any comp</h1>
    let header_content = <CompPreview roles={roles} specs={specs} placeholder={placeholder} />

    return header_content
}
