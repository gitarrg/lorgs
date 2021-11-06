import { useAppSelector } from "../../store/store_hooks"
import { get_current_user } from "../../store/user"

/**
 * Hook to get the currenty logged in user
 */
export default function useUser() {
    return useAppSelector(get_current_user)
}

