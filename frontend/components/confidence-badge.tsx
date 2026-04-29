import { Shield, AlertTriangle, ShieldOff, CheckCircle2 } from "lucide-react";
import { cn } from "@/lib/cn";

const STYLES: Record<string, { color: string; label: string; icon: any }> = {
  high:    { color: "bg-sage-500/15 text-sage-600 border-sage-500/40",    label: "High confidence",    icon: CheckCircle2 },
  medium:  { color: "bg-saffron-500/15 text-saffron-600 border-saffron-500/40", label: "Medium confidence", icon: Shield },
  low:     { color: "bg-wine-500/15 text-wine-500 border-wine-500/40",     label: "Low confidence",     icon: AlertTriangle },
  refused: { color: "bg-ink-700/15 text-ink-700 border-ink-700/40 dark:text-bone-100", label: "No answer (refused)", icon: ShieldOff },
};

export function ConfidenceBadge({ value }: { value: string }) {
  const s = STYLES[value] ?? STYLES.medium;
  const Icon = s.icon;
  return (
    <span
      role="status"
      aria-label={s.label}
      className={cn("inline-flex items-center gap-1.5 px-2 py-0.5 text-xs font-medium rounded-full border",
                     s.color)}
    >
      <Icon size={12} />
      {s.label}
    </span>
  );
}
