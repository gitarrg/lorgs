import DiscordLogo from '../../assets/DiscordLogo'
import PatreonLogo from '../../assets/PatreonLogo'
import { DISCORD_LINK, PATREON_LINK, BUYMEACOFFEE_LINK } from '../../constants'

import style from "./IndexLink.scss"
import type { ReactNode } from 'react'


function LinkButton({url, children} : {url: string, children: ReactNode }) {
    return (
        <div className={`${style.link} grow-when-touched border bg-dark`}>
            <a href={url} target="_blank" rel="noopener">
                {children}
            </a>
        </div>
    )
}


export default function IndexLinks() {

    return (
        <div>
            <h4>Links:</h4>
            <div className={style.container}>

                <LinkButton url="/help">
                    <i className="fas fa-info-circle"></i>
                    <span>Help</span>
                </LinkButton>

                <LinkButton url={DISCORD_LINK}>
                    <DiscordLogo />
                    <span>Discord</span>
                </LinkButton>

                <LinkButton url={PATREON_LINK}>
                    <PatreonLogo />
                    <span>Patreon</span>
                </LinkButton>

                <LinkButton url={BUYMEACOFFEE_LINK}>
                    <span style={{marginLeft: "-2px"}}>☕ Buy me a Coffee</span>
                </LinkButton>

            </div>
        </div>
    )
}
