/* just the container for the settings */
export default function SettingsBar({children} : { children: JSX.Element[] } ) {

    return (
        <div className="d-flex flex-row flex-wrap align-items-end mb-2">
            {children}
        </div>
    )
}
