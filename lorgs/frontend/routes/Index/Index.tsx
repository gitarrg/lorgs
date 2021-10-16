
import React from 'react'
import { Link } from 'react-router-dom'
import IndexSpecs from './IndexSpecs'
import styles from "./Index.scss"
import IndexLinks from './IndexLinks'

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


const TOP_REPORTS = <div>
    <h3>Top Reports by Comp:</h3>
    <div className="bg-dark rounded border p-2">

        <Link to="/comp_ranking/search" className="hover_grow_source">
            <div className="d-flex align-items-center">
                <img className="icon-spec icon-m rounded mr-1 wow-border-heal hover_grow_target" src="/static/images/roles/heal.jpg" />
                <span>Comp Reports</span>
            </div>
        </Link>

        <small className="text-muted">(🚧 Work in progress. 🚧)</small>
    </div>
</div>



export default function Index() {

    return (
        <div className={`${styles.container} mt-5`}>
            <div className={styles.col_left}>
                {INFO_TEXT}
                {DISCLAIMER}
            </div>
            <div className={styles.col_right}>
                <IndexSpecs />
                {TOP_REPORTS}
                <IndexLinks />
            </div>
        </div>
    )
}
