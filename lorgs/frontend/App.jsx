
import React from "react"
import ReactTooltip from 'react-tooltip';
import { BrowserRouter as Router, Switch, Route} from 'react-router-dom';
import { Provider } from 'react-redux'

import CompRankings from "./routes/CompRankings.jsx"
import CompSearch from "./routes/CompSearch.jsx"
import SpecRankings from "./routes/SpecRankings.jsx"
import data_store from "./store/store.js"
import GlobalDataLoader from "./components/GlobalDataLoader.jsx";

////////////////////////////////////////////////////////////////////////////////
// APP
//

export default function App() {

    ////////////////////////
    // Output
    return (
        <Provider store={data_store}>
        <React.StrictMode>
            <ReactTooltip 
                delayShow={25}
                className="tooltip"
                effect="solid"
                disable={LORRGS_DEBUG}
            />

            <GlobalDataLoader />

            <Router>
                <Switch>
                    <Route path="/spec_ranking/:spec_slug/:boss_slug">
                        <SpecRankings />
                    </Route>

                    <Route path="/comp_ranking/search">
                        <CompSearch />
                    </Route>
                    <Route path="/comp_ranking/:boss_slug">
                        <CompRankings />
                    </Route>
                </Switch>
            </Router>
        </React.StrictMode>
        </Provider>
    )
}

ReactDOM.render(<App />, document.getElementById("app_root"));
