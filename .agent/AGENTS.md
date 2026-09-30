# Core Rules

## Safety Rules
- Never delete existing functionality without explicit justification.
- Never overwrite working code blindly.
- Never fabricate information.
- Never claim something works without verification.
- Never invent APIs, libraries, environment variables, database fields, or configuration.
- Never silently ignore errors.
- Never modify unrelated files.
- Never expose secrets.
- Never commit credentials, API keys, tokens, or private keys.

## Before Editing
Always:
1. Inspect the relevant files.
2. Understand the existing implementation.
3. Check git status/diff.
4. Identify dependencies.
5. Determine the smallest safe change.

## After Editing
Always:
1. Inspect the changed code.
2. Run appropriate tests.
3. Run lint/type checking when available.
4. Run build when appropriate.
5. Fix discovered errors.
6. Update ".agent/" documentation.
