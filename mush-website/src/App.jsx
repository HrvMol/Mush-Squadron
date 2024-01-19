import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Home, Database, Admin } from "./pages";
import { ScrollToTop } from "./components";

const App = () => {
  return (
    <div>
      <BrowserRouter>
        <ScrollToTop />
          <Routes>
            <Route index element={<Home />} />
            <Route path="/home" element={<Home />} />
            <Route path="/database" element={<Database />} />
            <Route path="/_" element={<Admin />} />
          </Routes>
          
      </BrowserRouter>
    </div>
  )
}

export default App