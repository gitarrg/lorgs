import styles from "./UserReportLoading.scss"
import { Fragment } from "react";
import { fetch_data } from "../../api";
import { useHistory, useLocation } from "react-router";
import { useInterval } from 'react-use';
import { PATREON_LINK } from "../../constants";


/** Frequency in ms how often to check for task status updates */
const TASK_CHECK_INVERVAL = 1000 // 500


/** status when the task is still in the queue.
 * may or may not be already executing... all we know is that its not completed
 */
const TASK_STATUS_PENDING = "pending"


async function get_task_status(queue: string, task_name : string) {
    if (task_name === "done") { return "done" }
    return fetch_data(`/api/tasks/${queue}/${task_name}`)
}


function InfoBlock({ params } : { params: any }) {

    const found_keys: string[] = [] // keeps track of keys we already had
    const info_elements: JSX.Element[] = [] // keeps track of keys we already had
    for (const key of params.keys()) {

        // make sure we only add each key once
        if (found_keys.includes(key)) { continue }
        found_keys.push(key)

        const values = params.getAll(key)
        const value = values.join(", ")

        info_elements.push(
            <Fragment key={key}>
                <span>{key}{ values.length > 1 ? "s" : ""}</span>
                <span>{value}</span>
            </Fragment>
        )
    }

    // Render
    return (
        <>
            {info_elements}
        </>
    )
}


export default function UserReportLoading() {

    const { search } = useLocation();
    let history = useHistory();

    const params = new URLSearchParams(search)
    const report_id = params.get("report_id")
    const task_name = params.get("task")
    const queue = params.get("queue") || ""


    ////////////////////////////
    // Callback
    async function update_status() {

        if (!task_name) { return }

        const info = await get_task_status(queue, task_name)
        console.log("checking task status", info)

        // still waiting
        if (info.status == TASK_STATUS_PENDING) { return }

        // go next!
        console.log("task completed!")

        // cleanup the url
        params.delete("report_id")
        params.delete("task")
        params.delete("queue")
        const rest_search = params.toString()
        const url = `/user_report/${report_id}?${rest_search}`
        history.push(url)
    }
    useInterval(update_status, TASK_CHECK_INVERVAL);


    ////////////////////////////
    // Render
    return (
        <div className={styles.wrapper}>
            <div className={styles.container}>
                <h1>
                    <i className="fas fa-circle-notch fa-spin mr-2"></i>
                    loading...
                </h1>

                <div className={styles.info}>
                    <InfoBlock params={params} />
                </div>


                { queue == "free" && 
                    <div className={styles.advert + " bg-dark mt-4 p-2 border rounded wow-border-druid"}>
                        <span>
                            Become a <a href={PATREON_LINK} target="_blank" className="wow-legendary"><strong>Patreon</strong></a> and get acces to the premium queue!
                        </span>
                    </div>
                }
            </div>
        </div>
    )
}
