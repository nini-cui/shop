export const oidcConfig = {
    authority: `${import.meta.env.VITE_AUTHENTIK_URL}/application/o/shop/`,
    client_id: import.meta.env.VITE_AUTHENTIK_CLIENT_ID,
    redirect_uri: import.meta.env.VITE_REDIRECT_URI,
    response_type: "code",
    scope: "openid profile email",

    onSigninCallback: () => {
    window.history.replaceState(
      {},
      document.title,
      window.location.pathname
    );
  },
};