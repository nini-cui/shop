import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "react-oidc-context";

function ProtectedRoute() {
  const auth = useAuth();

  if (auth.isLoading) {
    return <p>Loading...</p>;
  }

  if (auth.error) {
    return <p>Authentication error: {auth.error.message}</p>;
  }

  if (!auth.isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
}

export default ProtectedRoute;
