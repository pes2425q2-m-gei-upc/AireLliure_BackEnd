import logo from './airelliure.jpg';
import './App.css';

function App() {

  const handleSubmit = (e) => {
    e.preventDefault(); 
    const templateParams = {
      from_email: document.getElementById('input-email').value,
      message: 'Gracias por registrarte en nuestra aplicación. Ahora puedes disfrutar de los beneficios de la aplicación.',
    }

    emailjs
    .send(
      'service_vvgyp7v',
      'template_3ftdh0j',
      templateParams,
      'a6ar94PP1cnz6o7Yo'
    )
    .then((response) => {
      console.log('Email enviado correctamente', response);
    })
    .catch((error) => {
      console.log('Error al enviar el email', error);
    })
  }



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
        <input id="input-email" className="input-email" type="text" placeholder="example@mail.com" />
        <button onClick={handleSubmit}>Registrarse</button>
      </div>
    </div>
  );
}

export default App;
