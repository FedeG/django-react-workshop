# Step 10: React linter

[Back to step 9](https://gitlab.com/FedeG/django-react-workshop/tree/step9_python_linter)

**ESLint** is an open source JavaScript linting utility originally created by Nicholas C. Zakas in June 2013. Code linting is a type of static analysis that is frequently used to find problematic patterns or code that doesn’t adhere to certain style guidelines. There are code linters for most programming languages, and compilers sometimes incorporate linting into the compilation process.

JavaScript, being a dynamic and loosely-typed language, is especially prone to developer error. Without the benefit of a compilation process, JavaScript code is typically executed in order to find syntax or other errors. Linting tools like **ESLint** allow developers to discover problems with their JavaScript code without executing it.

The primary reason **ESLint** was created was to allow developers to create their own linting rules. **ESLint** is designed to have all rules completely pluggable. The default rules are written just like any plugin rules would be. They can all follow the same pattern, both for the rules themselves as well as tests. While **ESLint** will ship with some built-in rules to make it useful from the start, you’ll be able to dynamically load rules at any point in time.

**ESLint** is written using **Node.js** to provide a fast runtime environment and easy installation via **npm** or **yarn**.

## Install eslint

#### Update package.json dependencies
We use devDependencies because these dependencies are only development dependencies.
We need to add the following in our `workshop/front/package.json`:
```diff
"devDependencies": {
  "babel": "^6.23.0",
  "babel-core": "^6.26.0",
+ "babel-eslint": "^8.0.1",
  "babel-loader": "^6.4.1",
  "babel-plugin-transform-decorators-legacy": "^1.3.4",
  "babel-preset-es2015": "^6.24.1",
  "babel-preset-react": "^6.24.1",
  "babel-preset-stage-0": "^6.24.1",
  "react-test-renderer": "^16.0.0",
+ "eslint": "^4.8.0",
+ "eslint-html-reporter": "^0.5.2",
+ "eslint-import-resolver-node": "^0.3.1",
+ "eslint-plugin-import": "^2.7.0",
+ "eslint-plugin-jest": "^21.2.0",
+ "eslint-plugin-react": "^7.4.0",
  "webpack": "^1.12.13",
  "webpack-bundle-tracker": "0.0.93",
  "webpack-dev-server": "^1.14.1"
  ...
```

#### Update package.json scripts
We need to add the following in our `workshop/front/package.json`:
```diff
"scripts": {
     "start": "node server.js",
-    "react-devtools": "react-devtools"
+    "react-devtools": "react-devtools",
+    "eslint": "./node_modules/.bin/eslint --ext .jsx --ext .js src",
+    "eslint-report": "./node_modules/.bin/eslint -f node_modules/eslint-html-reporter/reporter.js -o report.html --ext .jsx --ext .js src || true"
   },
```

#### Install dependencies
```bash
# with docker
docker exec -it workshopjs yarn install

# without docker
cd workshop/front
yarn install
```

## Create .eslintrc.yaml
**.eslintrc.yaml** file have all rules for **eslint**.
I'll push my **.eslintrc.yaml** (in **workshop/front/.eslintrc.yaml**) but you could use:
- [eslint](http://rapilabs.github.io/eslintrc-generator/)
- or create **.eslintrc.yaml** with **eslint** command:
```bash
# with docker
docker exec -it workshopjs ./node_modules/.bin/eslint --init

# without docker
cd workshop/front
./node_modules/.bin/eslint --init
```

## Update gitignore
And finally we should update `.gitignore` file and add `workshop/front/report.html`.

## Result
At this point, you can run **eslint**.

#### Run eslint with console report
```bash
# with docker
docker exec -it workshopjs npm run eslint

# without docker
cd workshop/front
npm run eslint
```

##### Read eslint console report
**eslint** command returns:
```javascript
/src/workshop/front/src/components/Headline/index.js
  6:24  error  'children' is missing in props validation  react/prop-types

✖ 1 problem (1 error, 0 warnings)
```

#### Run eslint with html report
```bash
# with docker
docker exec -it workshopjs npm run eslint-report

# without docker
cd workshop/front
npm run eslint-report
```

##### Read eslint html report
Open **workshop/front/report.html** in your browser.

[Step 11: Python testing](https://github.com/mbrochh/django-reactjs-boilerplate/tree/step11_python_testing)
