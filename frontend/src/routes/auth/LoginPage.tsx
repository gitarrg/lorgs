import { get_current_user, login } from "../../store/user"
import { useAppDispatch, useAppSelector } from "../../store/store_hooks"
import { useEffect } from "react"
import { useHistory, useLocation } from "react-router"
import style from "./LoginPage.scss"


/** Page where users get redirected to, after login in. */
export default function LoginPage() {

    const { search } = useLocation()
    const history = useHistory()

    const dispatch = useAppDispatch()
    const user = useAppSelector(get_current_user)

    const search_params = new URLSearchParams(search)
    const code = search_params.get("code")

    /** if we got a code, use it to try logging in the user */
    useEffect(() => {
        if (!code) { return }
        dispatch(login(code))
    }, [code])

    /** once logged in, we go back to the start page */
    useEffect(() => {
        if (user.logged_in) {
            history.push("/")
        }
    }, [user.logged_in])


    /** display error messages */
    if (user.error) {
        return (
            <div className={style.container}>
                <h4>Oh.. something went wrong.</h4>
                <div className="text-danger d-flex flex-column align-items-start">
                    <div>{user.error}</div>
                    <div>{user.error_message}</div>
                </div>
            </div>
        )
    }

    return (
        <div className={style.container}>
            <h4>
                <i className="fas fa-circle-notch fa-spin mr-1"></i>
                <span>logging in...</span>
            </h4>
        </div>
    )
}
