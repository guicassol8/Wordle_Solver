import Letter from "./Letter";

type Props = {
    letters: string[];
    colors?: ("correct" | "present" | "absent")[];
    id: string;
};

export default function Word({ letters, colors, id }: Props) {
    return (
        <div id={id} className="flex gap-1 p-1 bg-slate-800">
            {letters.map((char, i) => (
                <Letter
                    key={i}
                    char={char}
                    color={colors ? colors[i] : undefined}
                    animated={colors ? colors[i] != "absent" : false}
                />
            ))}
        </div>
    );
}
