import type { ReactNode } from "react";

/* just the container for the settings */
export default function SettingsBar({children} : { children: ReactNode } ) {

    return (
        <div className="d-flex flex-row flex-wrap align-items-end mb-2 gap-2">
            {children}
        </div>
    )
}
