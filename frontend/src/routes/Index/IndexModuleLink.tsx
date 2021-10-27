import { Link } from 'react-router-dom'
import styles from "./IndexModuleLink.scss"

export default function IndexModuleLink({title="", url="", children=[] as JSX.Element[], className=""}) {


    return (
        <div className={`${className} d-flex align-items-start flex-column`}>
            <h3>{title}</h3>
            <Link to={url}>
                <div className={`${styles.container} bg-dark rounded border grow-when-touched p-2 gap-2 d-flex align-items-center`}>
                    {children}
                </div>
            </Link>


        </div>
    )
}
