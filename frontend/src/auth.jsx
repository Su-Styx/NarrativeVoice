import { createContext, useContext, useState } from "react";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => localStorage.getItem("nv_user"));

  const login = (username) => {
    localStorage.setItem("nv_user", username);
    setUser(username);
  };

  const logout = () => {
    localStorage.removeItem("nv_user");
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);