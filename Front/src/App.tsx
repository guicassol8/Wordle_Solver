import { useState } from "react";
import Wordle from "./components/Wordle";
import wordList from "./words.json";

const usedWords = new Set<string>();
let currentWordIndex = 0;

export default function App() {
  const [gameResult, setGameResult] = useState<"win" | "lose" | null>(null);
  const [resetKey, setResetKey] = useState(0);
  const [word, setWord] = useState(() => getNextWord());

  function getNextWord() {
    // Avança até encontrar uma palavra ainda não usada
    while (currentWordIndex < wordList.length) {
      const candidate = wordList[currentWordIndex].toUpperCase();
      currentWordIndex++;
      if (!usedWords.has(candidate)) {
        usedWords.add(candidate);
        return candidate;
      }
    }

    // Se todas foram usadas, reinicia ou lança erro
    return "XXXXX"; // ou lançar erro, ou exibir uma mensagem
  }

  function handleReset() {
    setGameResult(null);
    setResetKey(prev => prev + 1);
    setWord(getNextWord());
  }

  const bgColor =
    gameResult === "win"
      ? "bg-green-700"
      : gameResult === "lose"
        ? "bg-red-700"
        : "bg-black";

  return (
    <div
      className={`min-h-screen transition-colors duration-500 ${bgColor} flex items-center justify-center`}
    >
      <Wordle
        key={resetKey}
        onGameEnd={setGameResult}
        onResetRequested={handleReset}
        targetWord={word}
      />
    </div>
  );
}
