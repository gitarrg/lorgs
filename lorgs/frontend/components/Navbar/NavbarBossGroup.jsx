import { useSelector } from 'react-redux';

import NavbarBossButton from "./NavbarBossButton.jsx";
import NavbarGroup from './NavbarGroup.jsx';
import { get_bosses } from '../../store/bosses.js';


////////////////////////////////////////////////////////////////////////////////
export default function NavbarBossGroup() {
    const bosses = useSelector(state => get_bosses(state));

    return (
        <NavbarGroup className="navbar_boss">
            {Object.values(bosses).map(boss =>
                <NavbarBossButton key={boss.full_name_slug} boss={boss} />
            )}
        </NavbarGroup>
    );
}
