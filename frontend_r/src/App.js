import { useState, useEffect } from "react";
import './styles.css';
import Login from "./Login";
import Register from "./Register";
import Upload from "./Upload";
import Logout from "./Logout";

function App() {
  const [mode, setMode] = useState("login"); // login | register | upload | logout
  const [token, setToken] = useState(null);

  // Restore token on load
  useEffect(() => {
    const savedToken = localStorage.getItem("accessToken");
    if (savedToken) {
      setToken(savedToken);
      setMode("upload");
    }
  }, []);

  const handleLogin = (newToken) => {
    localStorage.setItem("accessToken", newToken);
    setToken(newToken);
    setMode("upload");
  };

  const handleLogout = () => {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("uploadHistory"); // 👈 THIS
    setToken(null);
    setMode("login");
  };


  return (
    <div className="app-container">
      <div className="card">
        <h2>Django CSV Analyzer</h2>

        {!token && mode === "login" && (
          <Login
            onLogin={handleLogin}
            onSwitchToRegister={() => setMode("register")}
          />
        )}

        {!token && mode === "register" && (
          <Register onSwitchToLogin={() => setMode("login")} />
        )}

        {token && mode === "upload" && (
          <>
            <button
              className="danger"
              onClick={() => setMode("logout")}
            >
              Logout
            </button>
            <Upload token={token} />
          </>
        )}

        {token && mode === "logout" && (
          <Logout onLogout={handleLogout} />
        )}
      </div>
    </div>
  );
}

export default App;
