import styles from "./Help.scss"

export default function HelpSidebar() {
    return (

        <div className={styles.sidebar}>

            <nav className="bg-dark border rounded p-2" aria-label="Main Help Nav">

                <a className="h4" href="#overview">Overview</a>

                <a className="h4" href="#timeline">Timeline</a>
                <nav aria-label="Timeline SubNav">
                    <a className="h5" href="#timeline_nav">Navigation</a>
                    <a className="h5" href="#timeline_boss">Boss Lane</a>
                    <a className="h5" href="#timeline_players">Player Names</a>
                    <a className="h5" href="#timeline_ruler">Markers</a>
                </nav>

                <a className="h4" href="#spells_toolbar">Spells Toolbar</a>
                <nav aria-label="Spells Toolbar SubNav">
                    <a className="h5" href="#spells_toolbar_display">Display</a>
                    <a className="h5" href="#spells_toolbar_spells">Spells</a>
                </nav>

                <a className="h4" href="#navigation">Navigation</a>
            </nav>

        </div>
    )
}
