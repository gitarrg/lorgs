import IndexModuleLink from "./IndexModuleLink";
import styles from "./Index.scss"

function UserReportIcon() {

    const icon_path = "./static/img/inv_inscription_80_scroll.jpg"

    return <img
    className={`${styles.user_report_icon} wow-border-artifact icon-l rounded`}
    src={icon_path}
    alt="user report icon"
    />
}


export default function IndexUserReport() {

    return (
        <IndexModuleLink title="Custom Report:" url="/user_report" className={styles.user_report_link}>
            <UserReportIcon />
            <span className="h2">Load Log</span>

            <div className={styles.new_container}>
                <span className={styles.new}>NEW!</span>
            </div>

        </IndexModuleLink>
    )
}
