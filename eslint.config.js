import eslint         from "@eslint/js";
import tseslint       from "@typescript-eslint/eslint-plugin";
import {defineConfig} from "eslint/config";
import importPlugin   from "eslint-plugin-import";
import unusedImports  from "eslint-plugin-unused-imports";
import globals        from "globals";

const javascriptFiles = ["**/*.{js,mjs,cjs}"];
const typescriptFiles = ["**/*.{ts,tsx,mts,cts}"];

export default defineConfig(
    {
        name: "openbook/ignores",
        ignores: [
            "node_modules/**",
            "**/*.d.ts",
            "sbom/**",
            "src/frontend/app/src/api-client/**",
            "src/frontend/app/src/auth-client/**",
        ],
    },
    {
        name: "openbook/javascript",
        files: javascriptFiles,
        extends: [eslint.configs.recommended],
        languageOptions: {
            ecmaVersion: 8,
            sourceType: "module",
            globals: {
                ...globals.node,
            },
        },
    },
    {
        name: "openbook/typescript",
        files: typescriptFiles,
        extends: [
            eslint.configs.recommended,
            importPlugin.flatConfigs.recommended,
            importPlugin.flatConfigs.typescript,
            tseslint.configs["flat/recommended"],
            // "plugin:@typescript-eslint/recommended-requiring-type-checking",
            //'plugin:prettier/recommended'
        ],
        languageOptions: {
            ecmaVersion: 8,
            sourceType: "module",
            globals: {
                ...globals.node,
            },
        },
        settings: {
            "import/resolver": {
                typescript: true,
            },
        },
        plugins: {
            "unused-imports": unusedImports,
        },
        rules: {
            "import/default": "off",
            "import/export": "warn",
            "import/namespace": "warn",
            "import/no-duplicates": "off",
            "import/no-named-as-default": "off",
            "import/no-named-as-default-member": "off",
            "import/no-unresolved": "warn",
            "import/order": "off",
            "no-extra-semi": "warn",
            "prefer-const": "off",
            "@typescript-eslint/explicit-function-return-type": "off",
            "@typescript-eslint/explicit-module-boundary-types": "off",
            "@typescript-eslint/no-empty-function": "off",
            "@typescript-eslint/no-explicit-any": "off",
            "@typescript-eslint/no-unused-vars": "off",
            "unused-imports/no-unused-imports": "warn",
            //'prettier/prettier': ['error', {}, {
            //  usePrettierrc: true
            //}]
        },
    },
);