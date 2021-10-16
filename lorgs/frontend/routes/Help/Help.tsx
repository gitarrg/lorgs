import HelpContent from "./HelpContent";
import HelpHeader from "./HelpHeader";
import HelpSidebar from "./HelpSidebar";
import styles from "./Help.scss"

export default function Help() {
    return (
        <div className={styles.outer_container}>
            <div className={styles.container}>
                <HelpHeader />

                <HelpSidebar />
                <HelpContent />
            </div>
        </div>
    )
}
