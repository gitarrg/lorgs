import styles from "./DomainInfo.scss"


/**
 * Temportary Message to inform people about the new domain
 */
export default function DomainInfo() {

    const hostname = window.location.hostname
    if (hostname.includes("lorrgs.io")) {
        return null;
    }

    return (
        <div className={styles.container}>
            <a href="http://www.lorrgs.io">
                <span>🍾🥳 Lorrgs can now be found at <strong>lorrgs.io</strong> 🥳🎉</span>
            </a>
        </div>
    )
}
