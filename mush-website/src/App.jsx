import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Home, Database } from "./pages";
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
          </Routes>
          
      </BrowserRouter>
    </div>
  )
}

export default App