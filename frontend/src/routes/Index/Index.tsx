
import DomainInfo from "../../components/DomainInfo"
import IndexCompsGroup from './IndexCompsGroup'
import IndexLinks from './IndexLinks'
import IndexSpecs from './IndexSpecs'
import IndexUserReport from "./IndexUserReport"
import LoginButton from "../auth/LoginButton"
import styles from "./Index.scss"
import { useTitle } from 'react-use'



const INFO_TEXT = <div>
    <h3>What is this?</h3>

    <div className="bg-dark rounded border p-2 text-wrap">
        <p>This website looks at the current <strong className="wow-astounding">top 50 logs for every spec</strong>&nbsp;
        and visualizes <em className="wow-mage">"relevant"</em> spells on an encounter timeline.</p>

        <p>This lets you easily compare multiple high performing logs against each other, concerning when they use various important cooldowns.</p>
        <strong className="wow-legendary">No more sifting through individual logs manually!</strong>
    </div>
</div> // info text


const DISCLAIMER = <div>
    <h4>⚠️Disclaimer</h4>
    <div className="bg-dark rounded p-2 pt-0 text-wrap wow-border-deathknight">
        <p><strong className="fs-5 text-white">Do not simply copy paste the timings you see here!</strong></p>
        <p>This page is meant to <strong className="wow-rogue">give you a reference</strong>,
        but you will have to&nbsp;<strong className="wow-deathknight">adapt your cooldowns</strong>&nbsp;
        based on your guild’s strats, setup, push timings and other variables.</p>

        <hr className="border-0" />

        <p>Just seeing what people are doing successfully will not make it work for you,
        <span className="wow-monk">unless you understand why</span>.</p>

        <p className="mb-0">By looking at the timelines represented here you should conclude something like:</p>

        <div className="ml-2">
            <em className="text-light">"If we 4 heal this fight and push to phase 2 before 2:54, then it’s possible to achieve what I'm seeing here".</em>
        </div>
    </div>
</div> // disclaimer


export default function Index() {

    useTitle("Lorrgs: Index")

    return <>

        <DomainInfo />

        <div className="mt-1 d-flex justify-content-end">
            <LoginButton />
        </div>

        <div className={`${styles.container} mt-4`}>
            <div className={styles.col_left}>
                {INFO_TEXT}
                {DISCLAIMER}
            </div>
            <div className={styles.col_right}>
                <IndexSpecs />
                <IndexCompsGroup />
                <IndexUserReport />

                <IndexLinks />
            </div>
        </div>

    </>
}
