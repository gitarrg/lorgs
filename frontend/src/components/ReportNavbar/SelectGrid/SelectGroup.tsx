import type { ReactNode } from "react"
import styles from "./SelectGrid.scss"


type SelectGroupProps = {
    icon: ReactNode;
    items: ReactNode;
}



export function SelectGroup({ icon, items }: SelectGroupProps) {
    return (
        <div className="d-flex flex-row align-items-start gap-1">
            {icon}
            <div className={styles.row__items__container}>
                {items}
            </div>
        </div>
    );
}
