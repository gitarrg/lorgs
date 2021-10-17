import { DISCORD_LINK, PATREON_LINK } from '../../constants'

import style from "./IndexLink.scss"


function LinkButton({url, children} : {url: string, children: (JSX.Element|string)[]}) {
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
                    <img src="/static/images/icons/discord_logo.svg" alt="discord logo" />
                    <span>Discord</span>
                </LinkButton>

                <LinkButton url={PATREON_LINK}>
                    <img src="/static/images/icons/patreon_logo.svg" alt="patreon logo" />
                    <span>Patreon</span>
                </LinkButton>


            </div>
        </div>
    )
}
