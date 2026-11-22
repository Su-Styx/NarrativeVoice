import { createContext, useContext, useEffect, useState } from "react";
import { get, post } from "./api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    localStorage.removeItem("nv_user"); // clear old stub
    (async () => {
      await get("/csrf/");
      const { data } = await get("/me/");
      setUser(data.user ?? null);
      setLoading(false);
    })();
  }, []);

  const login = (username) => setUser(username);

  const logout = async () => {
    await post("/logout/");
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);