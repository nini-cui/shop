
import { useEffect } from "react";
import { BrowserRouter, Routes, Route, useNavigate } from "react-router-dom";
import { useAuth } from "react-oidc-context";

import ProductsPage from "./components/pages/ProductsPage";
import ProductForm from "./components/products/ProductForm";
import AuthPage from "./components/auth/AuthPage";
import SignupComplete from "./components/auth/SignupComplete";
import ProtectedRoute from "./components/auth/ProtectedRoute";

function AppRoutes() {
  const auth = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (auth.isLoading || !auth.isAuthenticated) return;

    const returnTo = auth.user?.state?.returnTo;

    console.log("OIDC callback completed");
    console.log("Return path:", returnTo);

    if (returnTo === "/signup-complete") {
      navigate("/signup-complete", { replace: true });
    }
  }, [auth.isLoading, auth.isAuthenticated, auth.user, navigate]);

  return (
    <Routes>
      <Route path="/login" element={<AuthPage />} />

      <Route path="/signup-complete" element={<SignupComplete />} />

      <Route element={<ProtectedRoute />}>
        <Route path="/" element={<ProductsPage />} />
        <Route path="/products/create" element={<ProductForm />} />
      </Route>
    </Routes>
  );
}

function App() {
  return (
    <BrowserRouter>
      <AppRoutes />
    </BrowserRouter>
  );
}

export default App;
