# Android Quality Scripts for GitLab CI

Python scripts that convert Android quality tool reports into [GitLab Code Quality](https://docs.gitlab.com/ee/ci/testing/code_quality.html) format, enabling inline annotations in merge requests.

## Scripts

### `android_lint_to_codeclimate.py`

Converts Android Lint XML reports to GitLab Code Quality JSON.

**Dependencies:** `xmltodict`

```bash
pip install xmltodict
```

**Usage:**

```bash
python3 android_lint_to_codeclimate.py <lint-results.xml> <project-dir-prefix> > lint-codeclimate.json
```

**Example:**

```bash
python3 android_lint_to_codeclimate.py \
  app/build/reports/lint-results-stagingDebug.xml \
  $CI_PROJECT_DIR \
  > app/build/reports/lint.json
```

**Severity mapping** (Android Lint priority → Code Climate severity):

| Priority | Severity   |
|----------|------------|
| 1-2      | info       |
| 3-4      | minor      |
| 5-6      | major      |
| 7-8      | critical   |
| 9-10     | blocker    |

### `checkstyle_to_codeclimate.py`

Converts Checkstyle XML reports (used by Detekt, ktlint, and other tools) to GitLab Code Quality JSON.

**Usage:**

```bash
python3 checkstyle_to_codeclimate.py <checkstyle-report.xml> <output.json>
```

**Example:**

```bash
python3 checkstyle_to_codeclimate.py \
  build/reports/detekt/merge.xml \
  build/reports/detekt/codeclimate.json
```

**Severity mapping** (Checkstyle severity → Code Climate severity):

| Checkstyle | Code Climate |
|------------|--------------|
| error      | critical     |
| warning    | major        |
| info       | minor        |

## GitLab CI usage

```yaml
android-lint:
  stage: quality
  before_script:
    - pip3 install xmltodict
  script:
    - ./gradlew --no-daemon lint
  after_script:
    - python3 android_lint_to_codeclimate.py app/build/reports/lint-results-stagingDebug.xml $CI_PROJECT_DIR > app/build/reports/lint.json
  artifacts:
    reports:
      codequality: app/build/reports/lint.json

detekt:
  stage: quality
  script:
    - ./gradlew --no-daemon detekt reportMerge
  after_script:
    - python3 checkstyle_to_codeclimate.py build/reports/detekt/merge.xml build/reports/detekt/codeclimate.json
  artifacts:
    reports:
      codequality: build/reports/detekt/codeclimate.json
```
