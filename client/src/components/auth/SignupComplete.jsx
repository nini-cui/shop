
import { useEffect, useState } from "react";
import { useAuth } from "react-oidc-context";
import { useNavigate } from "react-router-dom";

function SignupComplete() {
  const auth = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState(null);
  const [redirectStarted, setRedirectStarted] = useState(false);
  const [signupStarted, setSignupStarted] = useState(false);

  async function completeSignup() {
    try {
      console.log("Calling POST /users/create_user");

      const response = await fetch(
        "http://localhost:8000/users/create_user",
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${auth.user.access_token}`,
          },
        }
      );

      console.log("Create user status:", response.status);

      if (!response.ok) {
        const detail = await response.text();
        throw new Error(detail || "Failed to create application user");
      }

      console.log("Local user created successfully");
      navigate("/", { replace: true });
    } catch (err) {
      console.error("Signup error:", err);
      setError(err.message);
      setSignupStarted(false);
    }
  }

  useEffect(() => {
    console.log("SignupComplete:", {
      isLoading: auth.isLoading,
      isAuthenticated: auth.isAuthenticated,
      hasUser: !!auth.user,
      hasAccessToken: !!auth.user?.access_token,
    });

    if (auth.isLoading) return;

    if (!auth.isAuthenticated || !auth.user?.access_token) {
      if (redirectStarted) return;

      console.log("No OIDC token. Starting authorization...");
      setRedirectStarted(true);

      auth.signinRedirect({
        state: { returnTo: "/signup-complete" },
      }).catch((err) => {
        console.error("OIDC redirect failed:", err);
        setError(err.message);
        setRedirectStarted(false);
      });

      return;
    }

    if (signupStarted) return;

    console.log("OIDC token available. Completing signup...");
    setSignupStarted(true);
    completeSignup();

  }, [
    auth.isLoading,
    auth.isAuthenticated,
    auth.user?.access_token,
    redirectStarted,
    signupStarted,
  ]);

  if (error) return <p>Registration failed: {error}</p>;

  return <p>Completing your registration...</p>;
}

export default SignupComplete;
