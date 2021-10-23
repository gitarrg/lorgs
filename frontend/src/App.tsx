import { StrictMode, lazy, Suspense } from "react"
import { render } from 'react-dom';
import { BrowserRouter as Router, Switch, Route} from 'react-router-dom';
import { Provider } from 'react-redux'
import data_store from "./store/store"
import GlobalDataLoader from "./components/GlobalDataLoader";

// Delayed Imports
const Admin = lazy(() => import("./routes/Admin/Admin"));
const CompRankings = lazy(() => import("./routes/CompRankings/CompRankings"));
const CompSearch = lazy(() => import("./routes/CompSearch"));
const Help = lazy(() => import("./routes/Help/Help"))
const Index = lazy(() => import("./routes/Index/Index"));
const SpecRankings = lazy(() => import("./routes/SpecRankings"));
const UserReportIndex = lazy(() => import("./routes/UserReportIndex/UserReportIndex"));
const UserReport = lazy(() => import("./routes/UserReport/UserReport"));
const UserReportLoading = lazy(() => import("./routes/UserReportLoading/UserReportLoading"));


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

                    {/* Spec Rankings */}
                    <Route path="/spec_ranking/:spec_slug/:boss_slug" component={SpecRankings} />

                    {/* Comp Rankings */}
                    <Route path="/comp_ranking/search" component={CompSearch} />
                    <Route path="/comp_ranking/:boss_slug" component={CompRankings} />

                    {/* User Reports */}
                    <Route path="/user_report/" exact={true} component={UserReportIndex} />
                    <Route path="/user_report/load" exact={true} component={UserReportLoading} />
                    <Route path="/user_report/:report_id" component={UserReport} />

                    {/* other routes */}
                    <Route path="/help" component={Help} />
                    <Route path="/lorgmin" component={Admin} />

                    {/* fallback --> Home */}
                    <Route path="/" component={Index} />

                </Switch>
                </Suspense>
            </Router>

        </StrictMode>
        </Provider>
    )
}

render(<App />, document.getElementById("app_root"));
