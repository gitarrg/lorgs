import style from "./LoginPage.scss"
import useUser from "./useUser"
import { DISCORD_LOGIN_URL, DISCORD_CLIENT_ID } from "../../constants"
import { Link } from "react-router-dom"


function get_login_url() {

    const login_url = new URL("/login", document.baseURI)
    login_url.protocol = "https:"
    login_url.hostname = login_url.hostname.replace("www.", "")

    const url = new URL(DISCORD_LOGIN_URL)
    url.searchParams.set("client_id", DISCORD_CLIENT_ID)
    url.searchParams.set("response_type", "code")
    url.searchParams.set("scope", "identify")
    url.searchParams.set("redirect_uri", login_url.toString())
    return url
}


export default function LoginButton() {

    const user = useUser()

    if (user.logged_in) {
        return <div>
            <span className="text-muted">logged in as: </span>
            <Link to="/user">{user.name}</Link>
        </div>
    }

    const url = get_login_url()
    return <a className={style.loginLink} href={url.toString()}>Login</a>
}
