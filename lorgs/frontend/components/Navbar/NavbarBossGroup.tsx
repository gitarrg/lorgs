import NavbarBossButton from "./NavbarBossButton";
import NavbarGroup from './NavbarGroup';
import { get_bosses } from '../../store/bosses';
import { useAppSelector } from '../../store/store_hooks';


////////////////////////////////////////////////////////////////////////////////
export default function NavbarBossGroup() {
    const bosses = useAppSelector(state => get_bosses(state));

    return (
        <NavbarGroup>
            {Object.values(bosses).map(boss =>
                <NavbarBossButton key={boss.full_name_slug} boss={boss} />
            )}
        </NavbarGroup>
    );
}
