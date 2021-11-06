import { useEffect } from "react";
import { useAppDispatch } from "../../store/store_hooks"
import { load_user } from "../../store/user";

/**
 * Just a hook to load our user
 */
export default function UserProvider() {

    const dispatch = useAppDispatch()

    useEffect(() => {
        dispatch(load_user())
    }, [])

    return null
}
