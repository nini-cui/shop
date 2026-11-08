import { Navigate } from "react-router-dom";
import { useAuth } from "react-oidc-context";

function Login() {
  const auth = useAuth();

  if (auth.isLoading) {
    return <p>Loading...</p>;
  }

  if (auth.isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  return (
    <div>
      <h1>G'day</h1>
      <button onClick={() => auth.signinRedirect()}>Login</button>
    </div>
  );
}

export default Login;
