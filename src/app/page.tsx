import Image from 'next/image'

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between main">
      <div className="body">
        <div id='header'>
          <div className="titleNavbar">
            <img id='logo' src="logo.gif" alt="" />
            <img id='titulo' src="logo2Letra.jpg" alt="" />
          </div>
        </div>
      </div>
    </main>
  )
}
