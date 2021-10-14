
import { StrictMode } from "react"
import { render } from 'react-dom';
import { BrowserRouter as Router, Switch, Route} from 'react-router-dom';
import { Provider } from 'react-redux'

import CompRankings from "./routes/CompRankings"
import CompSearch from "./routes/CompSearch"
import SpecRankings from "./routes/SpecRankings"
import data_store from "./store/store"
import GlobalDataLoader from "./components/GlobalDataLoader";

////////////////////////////////////////////////////////////////////////////////
// APP
//

export default function App() {

    ////////////////////////
    // Output
    return (
        <Provider store={data_store}>
        <StrictMode>

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
        </StrictMode>
        </Provider>
    )
}

render(<App />, document.getElementById("app_root"));
