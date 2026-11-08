import { BrowserRouter, Routes, Route } from "react-router-dom";

import ProductsPage from "./components/pages/ProductsPage";
import ProductForm from "./components/products/ProductForm";
import Login from "./components/login/Login";
import ProtectedRoute from "./components/auth/ProtectedRoute";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />

        <Route element={<ProtectedRoute />}>
          <Route path="/" element={<ProductsPage />} />
          <Route path="/products/create" element={<ProductForm />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
