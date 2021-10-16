import { StrictMode, lazy, Suspense } from "react"
import { render } from 'react-dom';
import { BrowserRouter as Router, Switch, Route} from 'react-router-dom';
import { Provider } from 'react-redux'
import data_store from "./store/store"
import GlobalDataLoader from "./components/GlobalDataLoader";

// Delayed Imports
const Index = lazy(() => import("./routes/Index/Index"));
const CompRankings = lazy(() => import("./routes/CompRankings"));
const CompSearch = lazy(() => import("./routes/CompSearch"));
const SpecRankings = lazy(() => import("./routes/SpecRankings"));


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
                <Suspense fallback={<div>Loading...</div>}>
                <Switch>
                    <Route path="/spec_ranking/:spec_slug/:boss_slug" component={SpecRankings} />
                    <Route path="/comp_ranking/search" component={CompSearch} />
                    <Route path="/comp_ranking/:boss_slug" component={CompRankings} />
                    <Route path="/" component={Index} />
                </Switch>
                </Suspense>
            </Router>

        </StrictMode>
        </Provider>
    )
}

render(<App />, document.getElementById("app_root"));
