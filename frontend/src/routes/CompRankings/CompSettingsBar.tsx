/* SettingsBar for Comp Reports*/
import { Link } from 'react-router-dom';
import DisplaySettings from '../../components/SettingsBar/DisplaySettings'
import SettingsBar from '../../components/SettingsBar/SettingsBar'
import styles from "./CompSettingsBar.scss"
import SpellSettings from '../../components/SettingsBar/SpellSettings/SpellSettings';


export default function CompSettingsBar() {

    // Render
    return (
        <SettingsBar>
            <DisplaySettings />
            <SpellSettings />

            <div className="flex-grow-1"/>
            <Link
                to="/comp_ranking/search"
                className={`${styles.search_button} btn btn-primary shadow`}
            >
                Search
            </Link>

        </SettingsBar>
    )
}
