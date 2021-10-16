/**Spinner Overlay to indicate when things are loading */
import styles from "./LoadingOverlay.scss"

export default function LoadingOverlay() {
    return (
        <div className={`${styles.overlay} h1 shadow`}>
            <i className="fas fa-circle-notch fa-spin"></i>
            <span> loading..</span>
        </div>
    )
}
