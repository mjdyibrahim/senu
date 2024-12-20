import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './components/**/*.{vue,js}',
    './layouts/**/*.vue',
    './pages/**/*.vue',
    './plugins/**/*.{js,ts}',
    './nuxt.config.{js,ts}',
    './assets/css/**/*.{css,scss}', // Scan custom CSS files
  ],
  theme: {
    extend: {
      colors: {
        'accent-purple': 'rgb(89, 79, 238)',
        'background-light': 'rgb(254, 253, 250)',
        'primary-dark': 'rgb(27, 0, 48)',
        'primary-light': 'rgb(255, 255, 255)',
        'text-gray': 'rgb(69, 62, 74)',
      },
    },
  },
  plugins: [],
};

export default config;
