import next from "eslint-config-next";

export default [
  // Next.js recommended rules, including core-web-vitals when applicable
  ...next,
  {
    rules: {
      // Match previous .eslintrc.cjs behavior
      "@typescript-eslint/no-unused-vars": [
        "warn",
        { argsIgnorePattern: "^_", varsIgnorePattern: "^_" }
      ],
    },
    ignores: [
      "**/.next/**",
      "**/dist/**",
      "**/node_modules/**"
    ],
  },
];