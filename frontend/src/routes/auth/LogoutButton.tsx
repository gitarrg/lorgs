import { logout } from '../../store/user'
import { useAppDispatch } from '../../store/store_hooks'
import { useHistory } from 'react-router'

export default function LogoutButton() {

    const dispatch = useAppDispatch()
    const history = useHistory()

    function handle_logout() {
        dispatch(logout())
        history.push("/")
    }

    return (
        <button
            className="button button-grey grow-when-touched rounded border h3 text-white"
            onClick={handle_logout}>
            logout
        </button>
    )
}
