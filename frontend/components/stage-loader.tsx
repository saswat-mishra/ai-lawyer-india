"use client";
import { motion, AnimatePresence } from "framer-motion";

const STAGES = [
  "Reading the question",
  "Identifying jurisdiction & governing law",
  "Pulling controlling sections",
  "Cross-checking case authority",
  "Verifying citations",
];

/**
 * Visible per-stage loader. The point is honesty: the user sees the agent
 * doing real work, not a generic spinner.
 */
export function StageLoader({ active }: { active: boolean }) {
  if (!active) return null;
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0 }}
      className="rounded-xl border border-black/10 dark:border-white/10 p-4 bg-bone-50/60 dark:bg-ink-900/40 backdrop-blur"
    >
      <div className="text-xs uppercase tracking-wider text-ink-900/50 dark:text-bone-50/60 mb-3">
        Working
      </div>
      <ul className="space-y-2">
        {STAGES.map((s, i) => (
          <motion.li
            key={s}
            initial={{ opacity: 0, x: -6 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.18 }}
            className="flex items-center gap-2 text-sm"
          >
            <span className="h-1.5 w-1.5 rounded-full bg-saffron-500 animate-pulse" />
            {s}
          </motion.li>
        ))}
      </ul>
    </motion.div>
  );
}
