import FightSelectList from './FightSelectList'
import PlayerSelectList from './PlayerSelectList'
import ReportNavbarPlayerSelect from './ReportNavbarPlayerSelect'
import ReportNavbarPullSelect from './ReportNavbarPullSelect'
import { ReportNavbarLoadButton } from './ReportNavbarLoadButton'
import { useState } from 'react'

// @ts-ignore
import styles from "./ReportNavbar.scss"


export default function ReportNavbar() {

    const [collapsed, set_collapsed] = useState(false)
    const toggle_collapsed = () => (set_collapsed(!collapsed))

    return (
        <div className={styles.container}>

            <ReportNavbarPullSelect onClick={toggle_collapsed} />
            { !collapsed ? <FightSelectList /> : <div /> }

            <ReportNavbarPlayerSelect />
            { !collapsed ? <PlayerSelectList /> : <div /> }

            <ReportNavbarLoadButton />
        </div>
    )
}
