/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html, ts, scss}"
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require("daisyui"),

  ],

  daisyui: {
    styled: true,
    themes: true,
    base: true,
    utils: true,
    logs: true,
  }
}

