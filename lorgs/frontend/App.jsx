
import React from "react"
import { BrowserRouter as Router, Switch, Route} from 'react-router-dom';
import { Provider } from 'react-redux'

import AppContext from "./AppContext/AppContext.jsx"
import CompRankings from "./routes/CompRankings.jsx"
import SpecRankings from "./routes/SpecRankings.jsx"
import data_store from "./data_store.js"

////////////////////////////////////////////////////////////////////////////////
// APP
//

export default function App() {

    ////////////////////////
    // Output

    return (
        <Provider store={data_store}>
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
        </Provider>
    )
}

ReactDOM.render(<App />, document.getElementById("app_root"));
