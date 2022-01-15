import GlobalDataLoader from "./components/GlobalDataLoader";
import UserProvider from "./routes/auth/UserProvider";
import data_store from "./store/store"
import { BrowserRouter as Router, Switch, Route, Redirect } from 'react-router-dom';
import { Provider } from 'react-redux'
import { StrictMode, lazy, Suspense } from "react"
import { render } from 'react-dom';

// Delayed Imports
const Admin = lazy(() => import("./routes/Admin/Admin"));
const CompRankings = lazy(() => import("./routes/CompRankings/CompRankings"));
const CompSearch = lazy(() => import("./routes/CompSearch"));
const Help = lazy(() => import("./routes/Help/Help"))
const Index = lazy(() => import("./routes/Index/Index"));
const LoginPage = lazy(() => import("./routes/auth/LoginPage"));
const SpecRankings = lazy(() => import("./routes/SpecRankings"));
const UserPage = lazy(() => import("./routes/auth/UserPage"));
const UserReport = lazy(() => import("./routes/UserReport/UserReport"));
const UserReportIndex = lazy(() => import("./routes/UserReportIndex/UserReportIndex"));
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
            <UserProvider />

            <Router>
                <Suspense fallback={<div>Loading...</div>}>
                <Switch>

                    {/* Spec Rankings */}
                    <Route path="/spec_ranking/:spec_slug/:boss_slug/:difficulty" component={SpecRankings} />
                    <Route path="/spec_ranking/:spec_slug/:boss_slug" component={SpecRankings} />

                    {/* Comp Rankings */}
                    <Route exact path="/comp_ranking/search" component={CompSearch} />
                    <Route exact path="/comp_ranking/:boss_slug" component={CompRankings} />

                    {/* User Reports */}
                    <Route exact path="/user_report/load" component={UserReportLoading} />
                    <Route exact path="/user_report/:report_id" component={UserReport} />
                    <Route exact path="/user_report" component={UserReportIndex} />

                    <Route exact path="/login" component={LoginPage} />
                    <Route exact path="/user" component={UserPage} />

                    {/* other routes */}
                    <Route exact path="/help" component={Help} />
                    <Route exact path="/lorgmin" component={Admin} />

                    {/* fallback --> Home */}
                    <Route exact path="/" component={Index} />
                    <Redirect to="/" />

                </Switch>
                </Suspense>
            </Router>

        </StrictMode>
        </Provider>
    )
}

render(<App />, document.getElementById("app_root"));
