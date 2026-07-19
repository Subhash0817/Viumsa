import viumsaLogo from './assets/brand/viumsa_logo.png'
import './App.css'

function App() {
  return (
    <main className="viumsa-app">
      <section className="welcome">
        <div className="viumsa-mark">
          <img
            src={viumsaLogo}
            alt="Viumsa logo"
            className="viumsa-logo"
          />
        </div>

        <h1>VIUMSA</h1>

        <p className="tagline">
          Learn. Teach. Explore. Together.
        </p>
      </section>
    </main>
  )
}

export default App