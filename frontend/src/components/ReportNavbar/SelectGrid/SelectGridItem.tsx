import styles from "./SelectGrid.scss"
import { useFormContext, useWatch } from 'react-hook-form'
import { useContext, useEffect } from "react";
import { SelectGroupContext } from "./SelectGroup";
import useUser from "../../../routes/auth/useUser";


type SelectGridItemProps = {

    field_name: string
    className?: string
    children: JSX.Element | JSX.Element[]
}



export default function SelectGridItem({field_name, className="", children}: SelectGridItemProps) {

    ////////////////////////////////
    // Hooks
    const selected = useWatch({ name: field_name });
    const { setValue } = useFormContext();
    const group_selected = useContext(SelectGroupContext)

    const user = useUser()
    const user_can_multiselect = user.permissions.includes("user_reports")
    const field_parent = field_name.split("[")[0]

    ////////////////////////////////
    // Callbacks
    function onClick() {

        // force deseletion for free users
        if (!user_can_multiselect) {
            setValue(field_parent, [])
        }

        setValue(field_name, !selected)
    }

    // pass values when the group itself gets selected
    useEffect(() => {
        setValue(field_name, group_selected)
    }, [group_selected])

    ////////////////////////////////
    // Render
    return (
        <div
            className={`${styles.item__container} ${className} bg-dark border rounded ${selected ? "selected" : ""}`}
            onClick={onClick}
        >
            {children}
        </div>
    )
}
