import HeaderLogo from '../../components/HeaderLogo'
import styles from "./Help.scss"

export default function HelpHeader() {
    return (
        <h1 className={`${styles.header} m-0 mb-2 mt-3 d-flex align-items-center`}>
            <HeaderLogo wow_class="wow-priest" />
            <span className="ml-2">How to Lorrg:</span>
        </h1>
    )
}
