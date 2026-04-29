"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { MessageSquare, FileText, Building2, BookOpenText, Sparkles } from "lucide-react";
import { useSession } from "@/lib/session";
import { cn } from "@/lib/cn";

const NAV = [
  { href: "/", label: "Chat", icon: MessageSquare },
  { href: "/drafts", label: "Drafts & Notices", icon: FileText },
  { href: "/research", label: "Research", icon: BookOpenText },
  { href: "/company", label: "Company KB", icon: Building2 },
];

export function Sidebar() {
  const path = usePathname();
  const { persona, setPersona, ready } = useSession();
  return (
    <aside className="w-64 shrink-0 border-r border-black/10 dark:border-white/10 px-4 py-6 hidden md:flex flex-col gap-6">
      <div className="flex items-center gap-2">
        <Sparkles className="text-saffron-500" size={20} />
        <span className="font-serif text-lg font-semibold tracking-tight">Vakeel.ai</span>
        <span className="ml-auto text-[10px] uppercase tracking-widest text-muted-foreground opacity-70">India</span>
      </div>

      <nav className="flex flex-col gap-1">
        {NAV.map(({ href, label, icon: Icon }) => {
          const active = path === href || (href !== "/" && path.startsWith(href));
          return (
            <Link
              key={href}
              href={href}
              className={cn(
                "flex items-center gap-2 px-2.5 py-2 rounded-lg text-sm transition-colors",
                active
                  ? "bg-ink-900/5 dark:bg-white/10 text-ink-900 dark:text-bone-50"
                  : "text-ink-900/70 dark:text-bone-50/70 hover:bg-ink-900/5 dark:hover:bg-white/5",
              )}
            >
              <Icon size={16} />
              {label}
            </Link>
          );
        })}
      </nav>

      <div className="mt-auto">
        <div className="text-xs text-ink-900/50 dark:text-bone-50/50 mb-2">I am a…</div>
        <div className="grid grid-cols-3 gap-1 text-xs">
          {(["citizen", "founder", "practitioner"] as const).map(p => (
            <button
              key={p}
              disabled={!ready}
              onClick={() => setPersona(p)}
              className={cn(
                "px-2 py-1.5 rounded-md border transition",
                persona === p
                  ? "bg-saffron-500 text-white border-saffron-600"
                  : "border-black/10 dark:border-white/10 hover:bg-black/5 dark:hover:bg-white/5",
              )}
            >
              {p}
            </button>
          ))}
        </div>
        <div className="mt-3 text-[11px] text-ink-900/50 dark:text-bone-50/50 leading-snug">
          Information & document assistance, not legal advice. Consult an enrolled advocate for high-stakes matters.
        </div>
      </div>
    </aside>
  );
}
