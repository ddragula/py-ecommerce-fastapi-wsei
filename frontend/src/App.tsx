import Auth from "./components/Auth/Auth"
import { Content } from "./components/Content/Content"
import { Header } from "./components/Header/Header"
import { HashRouter as Router, Routes, Route } from "react-router-dom"
import { MainPage } from "./pages/Main";
import { Basket } from "./pages/Basket";
import { Orders } from "./pages/Orders";


function App() {
    return (
        <Router>
            <Header />
            <Content>
                <Routes>
                    <Route path="/" element={<MainPage />} />
                    <Route path="/login" element={<Auth type="login" />} />
                    <Route path="/register" element={<Auth type="register" />} />
                    <Route path="/basket" element={<Basket />} />
                    <Route path="/orders" element={<Orders />} />
                </Routes>
            </Content>
        </Router>
    );
}

export default App
