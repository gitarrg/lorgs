import { useAppSelector } from "../../store/store_hooks"
import { get_current_user } from "../../store/user"



export default function useUser() {

    const user = useAppSelector(get_current_user)
    return user

}

