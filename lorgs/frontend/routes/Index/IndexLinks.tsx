import React from 'react'

import style from "./IndexLink.scss"


const LINK_DISCORD = "https://discord.gg/jZWj6djJk2"


/** pass the icon as the one and only child */
function Link(
    {   url,
        disabled=false,
        children,
        tooltip=""
    } : {
        url: string,
        disabled?: boolean,
        children: (JSX.Element|string)[]
        tooltip?: string
    }) {

    return (
        <a href={url}>
            <div
                className={`${style.link} btn btn-lg ${disabled ? "disabled": ""} ${disabled ? "" : "grow-when-touched"} border bg-dark`}
                data-tooltip={tooltip}>
                <span>
                    {children}
                </span>
            </div>
        </a>
    )
}


export default function IndexLinks() {

    return (
        <div>
            <h4>Links:</h4>
            <div className={style.container}>

                <Link url="/help" disabled={true} tooltip="under construction">
                    <i className="fas fa-info-circle mr-1"></i>
                    Help
                </Link>

                <Link url={LINK_DISCORD}>
                    <img className="icon-s discord_logo mr-1" src="/static/images/icons/logo_discord.svg" alt="discord logo" />
                    Discord
                </Link>
            </div>
        </div>
    )
}
