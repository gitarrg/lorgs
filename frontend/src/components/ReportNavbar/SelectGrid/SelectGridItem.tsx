import styles from "./SelectGrid.scss"
import { useFormContext, useWatch } from 'react-hook-form'


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


    ////////////////////////////////
    // Callbacks
    function onClick() {
        setValue(field_name, !selected)
    }


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
