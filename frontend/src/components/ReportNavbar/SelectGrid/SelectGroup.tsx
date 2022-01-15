import { ReactNode, useState } from "react"
import { createContext } from "react"
import useUser from "../../../routes/auth/useUser"
import styles from "./SelectGrid.scss"


export const SelectGroupContext = createContext<boolean>(false)


type SelectGroupProps = {
    icon: ReactNode;
    items: ReactNode;
}


export function SelectGroup({ icon, items }: SelectGroupProps) {

    const [value, setValue] = useState(false)

    const user = useUser()
    const user_can_multiselect = user.permissions.includes("user_reports")

    function onClick() {
        user_can_multiselect && setValue(value => !value)
    }


    return (
        <div className={`${styles.icon} ${value ? styles.icon__selected : "" } d-flex flex-row align-items-start gap-1`}>

            <div onClick={onClick} >
                {icon}
            </div>

            <div className={styles.row__items__container}>
                <SelectGroupContext.Provider value={value}>
                    {items}
                </SelectGroupContext.Provider>
            </div>
        </div>
    );
}
