import styles from "./FaButton.scss"

/**
 * a Button using an FontAwesome Icon
 */
export default function FaButton({icon_name, tooltip="", disabled=false, onClick} : {icon_name: string; tooltip?: string, disabled: boolean, onClick: Function}) {

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



