/* just the container for the settings */
import React from 'react'


export default function SettingsBar({children}) {

    return (
        <div className="settings_bar d-flex flex-row align-items-end flex-wrap mb-2">
            {children}
        </div>
    )
}
