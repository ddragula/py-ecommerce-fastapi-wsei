import Auth from "./components/Auth"
import { Header } from "./components/Header"
import { BrowserRouter as Router, Routes, Route } from "react-router-dom"


function App() {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<div>Home</div>} />
        <Route path="/login" element={<Auth type="login" />} />
        <Route path="/register" element={<Auth type="register" />} />
      </Routes>
    </Router>
  )
}

export default App
