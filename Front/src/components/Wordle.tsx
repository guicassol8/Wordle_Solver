import { useEffect, useState } from "react";
import Word from "./Word";

const MAX_ATTEMPTS = 6;

type Props = {
    onGameEnd?: (result: "win" | "lose") => void;
    onResetRequested?: () => void;
    targetWord: string;
};

export default function Wordle({ onGameEnd, onResetRequested, targetWord }: Props) {
    const [guesses, setGuesses] = useState<string[]>([]);
    const [currentGuess, setCurrentGuess] = useState("");
    const [gameOver, setGameOver] = useState<null | "win" | "lose">(null);

    useEffect(() => {
        const handleKeyPress = (e: KeyboardEvent) => {
            const key = e.key.toUpperCase();

            if (key === "ENTER") {
                onResetRequested?.();
            }

            if (key === "BACKSPACE") {
                setCurrentGuess((prev) => prev.slice(0, -1));
            } else if (/^[A-Z]$/.test(key) && currentGuess.length < 5) {
                const next = currentGuess + key;
                if (next.length === 5) {
                    const nextGuesses = [...guesses, next];
                    setGuesses(nextGuesses);
                    setCurrentGuess("");

                    const isCorrect = next === targetWord;
                    const isLastTry = nextGuesses.length === MAX_ATTEMPTS;

                    if (isCorrect) {
                        setGameOver("win");
                        onGameEnd?.("win");
                    } else if (isLastTry) {
                        setGameOver("lose");
                        onGameEnd?.("lose");
                    }
                } else {
                    setCurrentGuess(next);
                }
            }
        };

        window.addEventListener("keydown", handleKeyPress);
        return () => window.removeEventListener("keydown", handleKeyPress);
    }, [currentGuess, guesses, gameOver, onGameEnd, onResetRequested]);

    // ... restante do componente permanece igual ...

    const colorize = (guess: string): ("correct" | "present" | "absent")[] => {
        const result: ("correct" | "present" | "absent")[] = Array(5).fill("absent");
        const used = Array(5).fill(false);

        for (let i = 0; i < 5; i++) {
            if (guess[i] === targetWord[i]) {
                result[i] = "correct";
                used[i] = true;
            }
        }

        for (let i = 0; i < 5; i++) {
            if (result[i] !== "correct") {
                for (let j = 0; j < 5; j++) {
                    if (!used[j] && guess[i] === targetWord[j]) {
                        result[i] = "present";
                        used[j] = true;
                        break;
                    }
                }
            }
        }

        return result;
    };

    return (
        <div className="flex flex-col gap-2 items-center">
            {guesses.map((guess, i) => (
                <Word
                    key={`guess-${i}`}
                    letters={guess.split("")}
                    colors={colorize(guess)}
                    id={`word${i + 1}`}
                />
            ))}

            {!gameOver && guesses.length < MAX_ATTEMPTS && (
                <Word
                    key="current"
                    letters={currentGuess.padEnd(5, " ").split("")}
                    id={`word${guesses.length + 1}`}
                />
            )}

            {[...Array(MAX_ATTEMPTS - guesses.length - (gameOver ? 0 : 1))].map((_, i) => (
                <Word
                    key={`empty-${i}`}
                    letters={["", "", "", "", ""]}
                    id={`word${guesses.length + (gameOver ? 1 : 2) + i}`}
                />
            ))}

            {gameOver && (
                <>
                    <p className="mt-4 text-white text-lg">
                        A palavra era: <span className="font-bold">{targetWord}</span>
                    </p>
                    <p className="mt-2 text-white text-sm italic">Pressione Enter para jogar novamente</p>
                </>
            )}
        </div>

    );
}
