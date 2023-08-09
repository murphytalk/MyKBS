import { type Component } from 'solid-js'
import bgImgUrl from './assets/kbs-bg.png'

const App: Component = () => {
  return (
    <div class="flex items-center justify-center h-screen bg-white">
      <div
        class="bg-cover bg-center bg-no-repeat bg-white w-full h-full flex flex-col justify-center items-center"
        style={{ 'background-image': `url(${bgImgUrl})` }}
      >
        <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 my-1 rounded-lg transform transition duration-300 hover:scale-105">
          My KBS
        </button>
        <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 my-1 rounded-lg transform transition duration-300 hover:scale-105">
          Free Chat
        </button>
      </div>
    </div>
  )
}

export default App
