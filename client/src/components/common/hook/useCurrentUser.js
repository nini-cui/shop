import { useState, useEffect } from "react";
import { useAuth } from "react-oidc-context";

function useCurrentUser() {
  const auth = useAuth();
  const [currentUser, setCurrentUser] = useState(null);

  async function fetchCurrentUser(accessToken) {
    try {
      const headers = {
        Authorization: `Bearer ${accessToken}`,
      };

      //   TODO: FIX THE LOGIC HERE
      const createUserResponse = await fetch(
        "http://localhost:8000/users/create_user",
        {
          method: "POST",
          headers,
        },
      );

      if (!createUserResponse.ok) {
        throw new Error("Failed to create user");
      }

      // Retrieve the application user and their roles
      const response = await fetch("http://localhost:8000/users/me", {
        headers,
      });

      if (!response.ok) {
        throw new Error("Failed to retrieve current user");
      }

      const data = await response.json();
      setCurrentUser(data);
    } catch (err) {
      console.error(err);
      setCurrentUser(null);
    }
  }

  useEffect(() => {
    if (auth.isLoading) return;

    if (!auth.isAuthenticated) {
      setCurrentUser(null);
      return;
    }

    fetchCurrentUser(auth.user.access_token);
  }, [auth.isLoading, auth.isAuthenticated, auth.user?.access_token]);

  return currentUser;
}

export default useCurrentUser;
