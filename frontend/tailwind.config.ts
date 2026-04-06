import type { Config } from "tailwindcss";

export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        console: {
          950: "#091119",
          900: "#101a26",
          850: "#182433",
          800: "#213044",
          700: "#32455e",
          600: "#4a6789",
          500: "#6c90b9",
          400: "#91b3d7",
        },
        success: "#38b56d",
        warning: "#f0b247",
        danger: "#ef5d5d",
        accent: "#48d1b2",
      },
      boxShadow: {
        panel: "0 10px 30px rgba(0, 0, 0, 0.28)",
      },
      fontFamily: {
        sans: ["IBM Plex Sans", "Segoe UI", "sans-serif"],
        mono: ["IBM Plex Mono", "Consolas", "monospace"],
      },
    },
  },
  plugins: [],
} satisfies Config;
