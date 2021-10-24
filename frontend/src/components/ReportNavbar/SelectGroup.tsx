

// @ts-ignore
import styles from "./SelectGroup.scss"


export function SelectGroup({ icon, items }) {
    return (
        <div className="d-flex flex-row align-items-start gap-1">
            {icon}
            <div className={styles.items_container}>
                {items}
            </div>
        </div>
    );
}
