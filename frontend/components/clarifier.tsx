"use client";
import { useState } from "react";

type Q = { slot: string; question: string; choices: string[]; allow_free_text?: boolean };

export function Clarifier({
  questions,
  onAnswer,
}: {
  questions: Q[];
  onAnswer: (slots: Record<string, string>) => void;
}) {
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const allFilled = questions.every(q => (answers[q.slot] ?? "").trim().length > 0);
  return (
    <div className="rounded-xl border border-saffron-500/40 bg-saffron-500/5 p-4">
      <div className="text-sm font-medium mb-3">A few quick details to make this accurate:</div>
      <div className="space-y-3">
        {questions.map(q => (
          <div key={q.slot} className="space-y-1.5">
            <label className="text-sm">{q.question}</label>
            <div className="flex flex-wrap gap-1.5">
              {q.choices.map(c => (
                <button
                  key={c}
                  type="button"
                  onClick={() => setAnswers(a => ({ ...a, [q.slot]: c }))}
                  className={
                    "px-2.5 py-1 text-xs rounded-md border transition " +
                    (answers[q.slot] === c
                      ? "bg-saffron-500 text-white border-saffron-600"
                      : "border-black/10 dark:border-white/15 hover:bg-black/5 dark:hover:bg-white/5")
                  }
                >
                  {c}
                </button>
              ))}
              {q.allow_free_text !== false && (
                <input
                  type="text"
                  className="text-xs px-2 py-1 rounded-md border border-dashed border-black/15 dark:border-white/15 bg-transparent w-40"
                  placeholder="or type"
                  value={answers[q.slot] ?? ""}
                  onChange={e => setAnswers(a => ({ ...a, [q.slot]: e.target.value }))}
                />
              )}
            </div>
          </div>
        ))}
      </div>
      <button
        disabled={!allFilled}
        onClick={() => onAnswer(answers)}
        className="mt-4 px-3 py-1.5 text-sm rounded-md bg-ink-900 text-bone-50 disabled:opacity-50"
      >
        Continue
      </button>
    </div>
  );
}
