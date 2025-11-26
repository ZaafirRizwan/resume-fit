import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/layout/Layout'
import Home from './pages/Home'
import AnalysisResult from './pages/AnalysisResult'
// import Dashboard from './pages/Dashboard'
// import Login from './pages/Login'

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Layout />}>
                    <Route index element={<Home />} />
                    <Route path="analysis/:id" element={<AnalysisResult />} />
                    {/* <Route path="dashboard" element={<Dashboard />} /> */}
                    {/* <Route path="login" element={<Login />} /> */}
                </Route>
            </Routes>
        </Router>
    )
}

export default App
