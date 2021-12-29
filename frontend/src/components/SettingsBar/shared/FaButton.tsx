import type { MouseEventHandler } from "react"
import styles from "./FaButton.scss"


type FaButtonProps = {

    icon_name: string;
    tooltip?: string,
    disabled?: boolean,
    onClick?: MouseEventHandler,
}

/**
 * a Button using an FontAwesome Icon
 */
export default function FaButton({icon_name, tooltip="", disabled=false, onClick} : FaButtonProps) {

    // avoid setting an empty attribute
    const tt = tooltip ? {"data-tooltip": tooltip} : {}

    return (
        <div {...tt}>
            <div
                className={`${styles.fa_button} button icon-s rounded border-white ${icon_name} ${disabled ? "disabled" : ""}`}
                onClick={onClick}
            />
        </div>
    )
}



