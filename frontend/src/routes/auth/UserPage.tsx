import HeaderLogo from '../../components/HeaderLogo'
import style from "./UserPage.scss"
import useUser from "./useUser"
import LogoutButton from "./LogoutButton"


export default function UserPage() {

    const user = useUser()


    return (
        <div className="content_center mt-5">

            <div className="d-flex flex-column">

            <h1 className="d-flex align-items-center gap-2">
                <HeaderLogo />
                <div>User:</div>
            </h1>

            <div className={`${style.user_info} bg-dark border rounded p-2 mb-2`}>
                <div>Name:</div><div>{user.name}</div>
                <div>ID:</div><div>{user.id}</div>
            </div>

            <LogoutButton />

            </div>
        </div>
    )
}
