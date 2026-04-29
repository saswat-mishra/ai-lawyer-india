import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        ink: { 950: "#0b0f17", 900: "#11151f", 800: "#1a1f2c", 700: "#252b3a" },
        bone: { 50: "#fbfaf6", 100: "#f5f3eb", 200: "#ece8d8" },
        saffron: { 500: "#e0823c", 600: "#c66c2a" },
        sage: { 500: "#6e8c6f", 600: "#587158" },
        wine: { 500: "#a23b3b", 600: "#852e2e" },
      },
      fontFamily: {
        serif: ['"Source Serif Pro"', 'Georgia', 'serif'],
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'monospace'],
      },
      animation: {
        "fade-up": "fade-up 0.4s ease-out",
        "shimmer": "shimmer 1.6s linear infinite",
      },
      keyframes: {
        "fade-up": {
          "0%": { opacity: "0", transform: "translateY(8px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        "shimmer": {
          "0%": { backgroundPosition: "-200% 0" },
          "100%": { backgroundPosition: "200% 0" },
        },
      },
    },
  },
  plugins: [],
};
export default config;
