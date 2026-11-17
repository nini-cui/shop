
import { useAuth } from "react-oidc-context";
import "./AuthPage.css";

function AuthPage() {
  const auth = useAuth();

  const handleSignUp = () => {
    window.location.href = "http://localhost:9000/if/flow/shop-enrollment/";
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h1>G'day!</h1>

        <div className="auth-buttons">
          <button
            className="auth-button login-button"
            onClick={() => auth.signinRedirect()}
            disabled={auth.isLoading}
          >
            Login
          </button>

          <button
            className="auth-button signup-button"
            onClick={handleSignUp}
          >
            Sign Up
          </button>
        </div>
      </div>
    </div>
  );
}

export default AuthPage;
