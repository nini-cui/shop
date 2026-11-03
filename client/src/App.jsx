import { BrowserRouter, Routes, Route } from "react-router-dom";
import ProductsPage from "./components/pages/ProductsPage";
import ProductForm from "./components/products/ProductForm";

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<ProductsPage />} />
          <Route path="/products/create" element={<ProductForm />} />
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
