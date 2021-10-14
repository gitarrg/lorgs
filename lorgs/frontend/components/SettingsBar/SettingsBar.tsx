/* just the container for the settings */
export default function SettingsBar({children} : { children: JSX.Element[] } ) {

    return (
        <div className="settings_bar d-flex flex-row align-items-end flex-wrap mb-2">
            {children}
        </div>
    )
}
