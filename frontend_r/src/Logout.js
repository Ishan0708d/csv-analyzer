function Logout({ onLogout }) {
  return (
    <div>
      <h3>Logout</h3>
      <p>Are you sure you want to log out?</p>
      <button className="danger" onClick={onLogout}>
        Yes, log me out
      </button>
    </div>
  );
}

export default Logout;
