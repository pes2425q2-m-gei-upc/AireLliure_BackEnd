import logo from './airelliure.jpg';
import './App.css';

function App() {
  return (
    <div className="App">
      <div className="title-container">
        <h1 className="title"> Aire Lliure</h1>
      </div>
      <div className="subtitle-container">
        <h2 className="subtitle">
          Respira llibertat, recorre el món amb aire net
        </h2>
      </div>
      <div className="logo-container">
        <img src={logo} alt="logo" />
      </div>
      <div className="form-container">
        <label className="form-label"> Descarrega la nostra aplicació a Android introduint el teu correu a continuació. </label>
        <br />
        <input className="input-email" type="text" placeholder="example@mail.com" />
        <button>Registrarse</button>
      </div>
    </div>
  );
}

export default App;
