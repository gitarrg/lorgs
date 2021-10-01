
import React from "react"
import { BrowserRouter as Router, Switch, Route} from 'react-router-dom';

import SpecRankings from "./SpecRankings.jsx"
import CompRankings from "./routes/CompRankings.jsx"
import AppContext from "./AppContext/AppContext.jsx"

////////////////////////////////////////////////////////////////////////////////
// APP
//

export default function App() {

    ////////////////////////
    // Output

    return (
        <React.StrictMode>
            <AppContext.AppContextProvider>
                <Router>
                    <Switch>
                        <Route path="/spec_ranking/:spec_slug/:boss_slug"> <SpecRankings /> </Route>
                        <Route path="/comp_ranking/:boss_slug"> <CompRankings /> </Route>
                    </Switch>
                </Router>
            </AppContext.AppContextProvider>
        </React.StrictMode>
    )
}

ReactDOM.render(<App />, document.getElementById("app_root"));
