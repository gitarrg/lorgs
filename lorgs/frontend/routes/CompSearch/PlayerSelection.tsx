/*
    Component to show the currently selected Roles/Specs
*/

import { useWatch } from "react-hook-form";
import CompPreview from '../../components/CompPreview';


export default function PlayerSelection() {

    // Fetch Form Vars
    const roles = useWatch({name: "comp.role"})
    const specs = useWatch({name: "comp.spec"})

    // Build Content
    let header_content = <CompPreview roles={roles} specs={specs} placeholder="any comp" />

    return header_content
}
