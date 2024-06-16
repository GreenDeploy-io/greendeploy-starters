# How to storybook


## How to install
inside `theme/static_src`,

1. run `nvm use`
2. run `npx sb init --type html`
3. when prompted to choose between Vite and Webpack5, choose Vite by default
   it looks like this:

    ```bash
    up to date, audited 127 packages in 532ms

    31 packages are looking for funding
    run `npm fund` for details

    found 0 vulnerabilities
    • Adding Storybook support to your "HTML" app?
    We were not able to detect the right builder for your project. Please select one: › - Use arrow-keys. Return to submit.
    ❯   Vite
        Webpack 5
    ```

4. when need to run the server, run `npm run storybook`
5. when prompted on what files to commit at git, commit any of the following:
    ```bash
    theme/static_src/.gitignore
    theme/static_src/.npmrc
    theme/static_src/.nvmrc
    theme/static_src/.storybook
    theme/static_src/package-lock.json
    theme/static_src/package.json
    theme/static_src/src/stories
    ```


This readme was constructed with help from ChatGPT taken from this [conversation](https://chat.openai.com/share/6a0711e8-6786-4e5a-b049-689d8c893291)

## How to run after installation

inside `theme/static_src`,

1. run `nvm use`
2. run `npm run storybook`