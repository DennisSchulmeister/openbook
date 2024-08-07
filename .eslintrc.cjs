/*
 * OpenBook Online: Interactive Online Textbooks
 * © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 */

module.exports = {
  root: true,
  env: {
    node: true,
    es6: true,
  },
  parserOptions: {
    ecmaVersion: 8,
    sourceType: "module",
  },
  ignorePatterns: ["node_modules/*", "**/*.d.ts"],
  extends: ["eslint:recommended"],
  plugins: ["@typescript-eslint", "unused-imports", "import"],
  overrides: [
    {
      files: ["**/*.ts"],
      parser: "@typescript-eslint/parser",
      settings: {
        "import/resolver": {
          typescript: {},
          node: {
            extensions: [".js", ".ts"],
          },
        },
      },
      env: {
        browser: false,
        node: true,
        es6: true,
      },
      extends: [
        "eslint:recommended",
        "plugin:import/errors",
        "plugin:import/warnings",
        "plugin:import/typescript",
        "plugin:@typescript-eslint/recommended",
        // "plugin:@typescript-eslint/recommended-requiring-type-checking",
        //'plugin:prettier/recommended'
      ],
      rules: {
        "import/default": "off",
        "import/no-named-as-default-member": "off",
        "import/no-named-as-default": "off",
        "import/no-unresolved": "warn",
        "import/export": "warn",
        "import/namespace": "warn",
        "import/order": "off",
        "import/no-duplicates": "off",
        "prefer-const": "off",
        "no-extra-semi": "warn",
        "@typescript-eslint/no-unused-vars": ["off"],
        "@typescript-eslint/explicit-function-return-type": ["off"],
        "@typescript-eslint/explicit-module-boundary-types": ["off"],
        "@typescript-eslint/no-empty-function": ["off"],
        "@typescript-eslint/no-explicit-any": ["off"],
        "unused-imports/no-unused-imports": "warn",
        //'prettier/prettier': ['error', {}, {
        //  usePrettierrc: true
        //}]
      },
    },
  ],
};
