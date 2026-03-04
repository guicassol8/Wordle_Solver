type Props = {
    char: string;
    color?: "correct" | "present" | "absent";
    index?: number;
    animated?: boolean;
};

export default function Letter({ char, color, index = 0, animated = false }: Props) {
    let bg = "bg-slate-950";
    if (color === "correct") bg = "bg-green-600";
    else if (color === "present") bg = "bg-yellow-500";
    else if (color === "absent") bg = "bg-slate-700";

    const delay = `${index * 150}ms`; // Cascata: 0ms, 150ms, 300ms...

    return (
        <div className="h-12 w-12 flex items-center justify-center perspective">
            <div
                className={`h-11 w-11 flex items-center justify-center text-white text-xl font-bold rounded shadow-md ${bg} ${animated ? "animate-flip" : ""
                    }`}
                style={{ animationDelay: delay }}
            >
                {char.toUpperCase()}
            </div>
        </div>
    );
}
