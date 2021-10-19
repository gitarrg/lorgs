
import { useRouteMatch, Route } from 'react-router-dom';
import { AdminHeader } from './AdminHeader';
import AdminNavbar from './AdminNavbar';
import AdminSpells from './AdminSpells';
import AdminStatus from './AdminStatus';


export default function Admin() {

    const { path }  = useRouteMatch()

    return (
        <div>

            <div className="mt-3 p-2">
                <AdminHeader />
            </div>
            <div>
                <AdminNavbar />
            </div>

            <div>

                <Route path={`${path}/status`}>
                    <AdminStatus />
                </Route>

                <Route path={`${path}/spells`}>
                    <AdminSpells />
                </Route>

            </div>
        </div>
    )
}
