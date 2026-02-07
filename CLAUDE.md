# General Development Best Practices

## API Integration - Always Check Latest Documentation

**CRITICAL**: When working with external APIs (non-standard library), ALWAYS search for latest documentation BEFORE implementing or debugging.

### Why This Matters
- APIs change frequently (new parameters, deprecations, behavior changes)
- Models and services add new features
- Old examples and assumptions lead to bugs, poor performance, and higher costs
- Beta APIs evolve rapidly

### Best Practice Workflow - Test-First Approach

When integrating with an external API, follow this disciplined workflow:

1. **Research First - WebFetch/WebSearch API Documentation**
   ```
   Search: "[API name] [feature] [current year] latest documentation"
   Example: "OpenAI chat completions API 2026 documentation"
   ```
   - Check official API reference documentation
   - Review official cookbooks and examples
   - Read changelog/release notes
   - Verify model/service-specific limitations

2. **Write Tests First - Before Any Implementation Code**
   ```python
   # Write comprehensive integration tests covering:
   # - Authentication/API key validation
   # - Main endpoints and expected responses
   # - Error cases (rate limits, invalid params, etc.)
   # - Edge cases specific to the API

   def test_api_authentication():
       assert client.authenticate() == True

   def test_main_endpoint():
       response = client.call_api(valid_params)
       assert response.status_code == 200

   def test_error_handling():
       with pytest.raises(APIError):
           client.call_api(invalid_params)
   ```

3. **Implement Client Code**
   - Write the actual API integration code
   - Use verified parameter names and values from documentation
   - Implement error handling for documented failure modes

4. **Iterate Until 100% Pass Rate**
   ```bash
   pytest -v  # Run after EVERY code change
   ```
   - **Autonomous debugging workflow:**
     - Test fails → Read error message carefully
     - Check API documentation again
     - Fix the code
     - Run `pytest -v` again
     - Repeat until all tests pass

   - **DO NOT ask for help** - debug autonomously by:
     - Reading tracebacks thoroughly
     - Checking latest API documentation
     - Testing one change at a time
     - Verifying assumptions with minimal test cases

5. **Complete Only When 100% Tests Pass**
   - All authentication tests pass
   - All endpoint tests pass
   - All error handling tests pass
   - No flaky or skipped tests

### Red Flags - Immediate Doc Check Required
⚠️ Check documentation when:
- API call runs slower than expected
- Parameters seem to have no effect
- Error messages mention unknown parameters
- Using beta/preview APIs
- Working with recently released models/services
- Seeing unexpected behavior after updates

### Example: Right Approach
```python
# ❌ WRONG: Assume old parameters work
api.call(model="new-model", old_param="value")

# ✅ RIGHT: Check docs first
# 1. Search: "new-model API parameters 2026"
# 2. Read official docs
# 3. Discover: old_param renamed to new_param
# 4. Implement correctly
api.call(model="new-model", new_param="value")
```

---

## Jupyter Notebooks - Execute and Validate

**Principle**: When working with Jupyter notebooks, ensure all cells execute successfully with current API versions. Don't just read notebooks—execute them end-to-end and fix any compatibility issues.

### Workflow for Notebook Updates

When asked to work with a Jupyter notebook, follow this systematic approach:

1. **Research Latest API Docs for Each Cell**
   ```bash
   # For each cell that uses external APIs (OpenAI, SGLang, etc.)
   # WebSearch: "[API name] [method] 2026 latest documentation"
   ```
   - Identify all external API calls in the notebook
   - WebSearch for latest documentation for each API
   - Note any deprecated parameters or methods

2. **Update Deprecated Parameters/Methods**
   ```python
   # Before (deprecated)
   client.completion(engine="davinci", max_tokens=100)

   # After (current API)
   client.chat.completions.create(model="gpt-4o", max_tokens=100)
   ```
   - Update parameter names (e.g., `engine` → `model`)
   - Update method names (e.g., `completion()` → `chat.completions.create()`)
   - Update model names to current versions
   - Fix import statements if API structure changed

3. **Execute the Notebook**
   ```bash
   jupyter nbconvert --to notebook --execute notebook.ipynb --output executed.ipynb
   ```
   - This executes every cell sequentially
   - Captures all outputs (text, images, dataframes)
   - Stops on first error with traceback

4. **Autonomous Debugging Loop**
   When execution fails:
   - **Read the traceback carefully** - identify which cell failed and why
   - **Research the fix** - WebSearch for the specific error or API method
   - **Update the cell** - fix the code in the original notebook
   - **Re-execute** - run nbconvert again
   - **Repeat** until entire notebook runs without errors

   **DO NOT ask for help** - debug autonomously:
   ```
   Error → Read traceback → Identify API issue → WebSearch docs → Fix code → Re-execute
   ```

5. **Document API Changes**
   Add markdown cells documenting what you discovered:
   ```markdown
   ## API Updates (2026)
   - Changed `openai.Completion.create()` → `openai.chat.completions.create()`
   - Parameter `engine` renamed to `model`
   - Model `text-davinci-003` deprecated, using `gpt-4o-mini`
   ```

6. **Save Fully-Executed Version**
   - Ensure `executed.ipynb` has all cell outputs visible
   - All text outputs, plots, dataframes should be rendered
   - No errors or warnings
   - Ready for review without needing to re-run

### Common Notebook Issues

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError` | Check if package name changed, update imports |
| `TypeError: unexpected keyword` | API parameter renamed, check latest docs |
| `Model not found` | Model deprecated, WebSearch current model names |
| `AuthenticationError` | Check if API key env var name changed |
| `RateLimitError` | Add retry logic or reduce request frequency |

### Success Criteria

✅ Notebook fully executed without errors
✅ All external API calls use current syntax
✅ All outputs visible (no empty cells)
✅ API changes documented in markdown cells
✅ executed.ipynb saved and committed

---

## Git Commit Discipline

**Principle**: Commit after each working feature or iteration. Create a history of working states, not a single massive commit at the end.

### When to Commit

**DO commit when:**
- ✅ A feature is complete and working (tests pass)
- ✅ An iteration is done (API integration, notebook execution, refactor)
- ✅ You've fixed a bug and verified the fix
- ✅ You've updated documentation that corresponds to working code
- ✅ Before starting a new feature or risky refactor

**DON'T commit when:**
- ❌ Tests are failing
- ❌ Code doesn't compile/run
- ❌ You're in the middle of implementing a feature
- ❌ You have commented-out debug code

### Commit Message Format

Write descriptive commit messages that explain **what** was completed:

**Good commit messages:**
```bash
git commit -m "Add OpenAI API client with authentication tests"
git commit -m "Update notebook to use GPT-4o API (deprecated text-davinci)"
git commit -m "Fix rate limit handling in API client"
git commit -m "Add error handling for invalid PDF inputs"
```

**Bad commit messages:**
```bash
git commit -m "updates"
git commit -m "fix"
git commit -m "wip"
git commit -m "changes"
```

### Commit Workflow

```bash
# 1. Verify feature works
pytest -v  # All tests pass
# or
python script.py  # Runs without errors
# or
jupyter nbconvert --execute notebook.ipynb  # Executes fully

# 2. Stage relevant files
git add file1.py file2.py

# 3. Commit with descriptive message
git commit -m "Add PDF form field extraction with pypdf integration

- Implements hybrid extraction (AcroForm + page annotations)
- Adds tests for multi-page PDFs
- Handles orphaned widget annotations"

# 4. Move to next feature
```

### Benefits of Frequent Commits

- **Rollback safety**: If next feature breaks, revert to last working state
- **Progress tracking**: Clear history of what was built when
- **Debugging**: Bisect commits to find when bug was introduced
- **Collaboration**: Others can pull working increments, not broken code
- **Documentation**: Commit history tells the story of development

### Commit Checklist

Before committing:
- [ ] Feature/fix is complete and working
- [ ] Tests pass (if applicable)
- [ ] No debug print statements or commented code
- [ ] Relevant files staged (not everything with `git add .`)
- [ ] Commit message describes what was accomplished
- [ ] Ready to start next feature from this state

---

## Minimize File Creation

**Principle**: Avoid creating new files unless absolutely necessary. Each new file adds maintenance overhead and fragments the codebase.

### What to Avoid

❌ **Don't create unnecessary files:**
- Multiple README files (README.md, README_INSTALLATION.md, README_USAGE.md, etc.)
- Separate documentation files for every feature
- Shell script wrappers for simple commands
- Multiple configuration files when one suffices
- Duplicate scripts with slight variations

✅ **Prefer instead:**
- Single README.md with clear sections
- Comments in code rather than separate doc files
- Direct commands in documentation rather than wrapper scripts
- Consolidate related configurations
- Parameterized scripts instead of duplicates

### Examples

**Bad - File Proliferation:**
```
README.md
README_INSTALLATION.md
README_USAGE.md
README_TROUBLESHOOTING.md
start-dev.sh
start-prod.sh
start-test.sh
setup-mac.sh
setup-linux.sh
```

**Good - Minimal Files:**
```
README.md                    # All documentation in one place with sections
start.sh --env [dev|prod]    # One script with parameters
setup.sh --os [mac|linux]    # Parameterized setup
```

### When New Files ARE Justified
- Core source code files (actual application logic)
- Test files (when following testing conventions)
- Configuration files required by tools (package.json, .gitignore, etc.)
- Large, distinct features that truly warrant separation

---

## Code Conciseness - Prefer Simplicity

**Principle**: When you can write 10 lines to complete a job, don't write 100 lines.

### Key Guidelines

1. **Avoid Over-Engineering**
   - Don't add features not requested
   - Don't create abstractions for one-time use
   - Don't add "future-proofing" for hypothetical requirements
   - Don't wrap simple operations in complex classes

2. **Appropriate Documentation**
   - ✅ DO: Add docstrings to public functions/classes
   - ✅ DO: Comment complex logic that isn't self-evident
   - ❌ DON'T: Comment obvious code
   - ❌ DON'T: Add documentation for every trivial operation

3. **Simplicity Over Cleverness**
   - Three similar lines > premature abstraction
   - Direct code > convoluted one-liner
   - Clear variable names > need for explanatory comments

### Examples

**Bad - Over-Documented Simple Code:**
```python
# Initialize the counter variable to zero
counter = 0

# Iterate through each item in the list
for item in items:
    # Increment the counter by one
    counter += 1

# Return the final count
return counter
```

**Good - Self-Evident Code:**
```python
return len(items)
```

**Bad - Over-Engineered:**
```python
class ConfigurationManager:
    """Manages application configuration."""

    def __init__(self):
        self.config = {}

    def set_value(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        self.config[key] = value

    def get_value(self, key: str) -> Any:
        """Get a configuration value."""
        return self.config.get(key)

# Used only once in entire codebase:
config = ConfigurationManager()
config.set_value("api_key", os.getenv("API_KEY"))
```

**Good - Simple and Direct:**
```python
API_KEY = os.getenv("API_KEY")
```

**Good - Documented Where Needed:**
```python
def extract_fields(pdf_path: str, dpi: int = 200) -> list[dict]:
    """
    Extract form fields from PDF.

    Uses hybrid approach: scans both AcroForm tree and page annotations
    to catch orphaned widget annotations that don't appear in field tree.

    Args:
        pdf_path: Path to PDF file
        dpi: Resolution for page rendering (higher = better quality, slower)

    Returns:
        List of field dictionaries with name, type, value, etc.
    """
    # Implementation details are self-documenting
    acroform_fields = reader.get_fields()
    annotation_fields = scan_page_annotations(reader)
    return merge_fields(acroform_fields, annotation_fields)
```

### When to Add More Code
✅ Justified complexity:
- Error handling at system boundaries (user input, external APIs)
- Security validation (input sanitization, authentication)
- Performance optimization for proven bottlenecks
- Public API design for libraries
- Complex business logic that requires explanation

❌ Unjustified complexity:
- Abstractions for single-use code
- Defensive programming for impossible states
- Configuration systems for fixed values
- Frameworks for simple scripts

---

## Code Consistency - Complete Ripple Updates

**Principle**: When changing a value, parameter, or name, update ALL occurrences.

### The Problem
Partial updates create:
- Inconsistent behavior across codebase
- Documentation that doesn't match reality
- Configuration mismatches
- User confusion

### The Solution - Systematic Updates

**Step 1: Find all occurrences**
```bash
grep -r "old_value" . --exclude-dir=.git
```

**Step 2: Update every location**
- Source code (all files)
- Configuration files
- Documentation (README, help text)
- Examples and code comments
- Error messages
- Scripts and wrappers

**Step 3: Verify consistency**
```bash
grep -r "old_value" .  # Should be empty
grep -r "new_value" .  # Should show all expected locations
```

### Checklist for Changes

When changing defaults, parameters, function names, or values:

- [ ] Search codebase for all occurrences
- [ ] Update source code (all files)
- [ ] Update configuration/wrapper scripts
- [ ] Update README and documentation
- [ ] Update examples in docs
- [ ] Update comments and docstrings
- [ ] Update help text and error messages
- [ ] Verify with grep that old value is gone
- [ ] Test from all entry points

---

## Documentation - Quality Over Quantity

**Principle**: Apply the same conciseness principle to documentation. Clear, scannable docs beat verbose walls of text.

### What Makes Good Documentation

✅ **Good Documentation:**
- Gets user to working state quickly
- Scannable headers and bullet points
- Concrete examples over abstract explanations
- Single README with clear sections > multiple README files
- Focused on "what" and "why", not obvious "how"

❌ **Bad Documentation:**
- Verbose prose that could be 3 bullet points
- Redundant information across multiple files
- Explanations of obvious concepts
- Walls of text without structure
- Over-documentation of trivial features

### Examples

**Bad - Verbose and Redundant:**
```markdown
# Installation Guide

This section will walk you through the process of installing the application.
Installation is an important first step before you can use the application.
Follow these steps carefully to ensure proper installation.

## Step 1: Prerequisites

Before you begin the installation process, you will need to make sure that
you have all the necessary prerequisites installed on your system. The
prerequisites are important because without them, the installation will not
succeed.

### Installing Python

Python is a programming language that is required to run this application...
(3 more paragraphs explaining what Python is)
```

**Good - Concise and Actionable:**
```markdown
# Installation

## Prerequisites
- Python 3.9+
- pip

## Install
```bash
pip install -r requirements.txt
python app.py
```

## Verify
```bash
curl http://localhost:8000/health
# Expected: {"status": "ok"}
```
```

### Documentation Structure Guidelines

**Single README Structure:**
```markdown
# Project Name
One-line description

## Quick Start (30 seconds to working state)
## Installation
## Usage
## Configuration (if needed)
## Troubleshooting (common issues only)
## API Reference (if library)
```

**Avoid Creating:**
- README_INSTALLATION.md (put in main README)
- USAGE.md (put in main README)
- EXAMPLES.md (put inline in README)
- ARCHITECTURE.md (unless truly complex system)
- CONTRIBUTING.md (unless open source with many contributors)

### When Verbose Docs ARE Justified

✅ Create detailed docs for:
- Complex APIs with many endpoints
- Systems with non-obvious architecture
- Security-critical configuration
- Migration guides (version X → Y)
- Troubleshooting unusual edge cases

❌ Don't create verbose docs for:
- Simple scripts or tools
- Self-explanatory code
- Standard installation procedures
- Common development patterns

### The README Test

Good README answers these questions in < 2 minutes:
1. What does this do?
2. How do I install it?
3. How do I use it?
4. Where do I get help?

If your README takes > 5 minutes to read, it's too long. Consider:
- Removing redundant sections
- Using collapsible sections for details
- Moving advanced topics to wiki/docs site
- Using more examples, fewer words

### Example: Before & After

**Before (200 lines):**
- Long introduction explaining problem space
- Detailed explanation of every feature
- Multiple installation guides for different OS
- Verbose troubleshooting for every possible error
- Full API documentation inline

**After (50 lines):**
- One-line problem statement + solution
- Quick start with working example
- Single installation command (script handles OS detection)
- Link to troubleshooting guide (separate doc)
- Link to API docs (separate if complex)

### Key Principle

> **Write documentation like code: keep it DRY (Don't Repeat Yourself), concise, and scannable. If it takes longer to read the docs than to read the code, you've documented too much.**

---

## General Principles Summary

### Core Workflows
1. **API Integration (Test-First)**: WebSearch docs → Write tests → Implement → `pytest -v` → Debug autonomously → 100% pass rate
2. **Jupyter Notebooks**: WebSearch APIs → Update deprecated code → Execute notebook → Debug autonomously → Document changes → Save executed version
3. **Git Commits**: Commit after each working feature/iteration with descriptive messages

### Code Quality
4. **Code Conciseness**: Prefer 10 lines over 100 when both accomplish the goal
5. **Documentation Quality > Quantity**: Clear, scannable docs beat verbose walls of text
6. **File Minimization**: Don't create new files unless absolutely necessary

### Development Discipline
7. **Autonomous Debugging**: Don't ask for help—read errors, check docs, fix code, repeat
8. **Consistency**: Update all occurrences when changing values
9. **Simplicity**: Avoid over-engineering and premature abstraction

---

## Quick Decision Framework

**Before creating a new file, ask:**
- Can this go in an existing file with a new section?
- Can this be inline documentation/comments instead?
- Is this required by a tool, or just "nice to have"?

**Before adding 50+ lines of code, ask:**
- Can this be done in 10 lines?
- Am I over-engineering for hypothetical future needs?
- Is this abstraction used more than once?

**Before integrating an external API, ask:**
- Have I WebSearched/WebFetched the latest official documentation?
- Have I written comprehensive tests first (auth, endpoints, errors)?
- Am I prepared to debug autonomously until tests pass?
- Have I verified current parameter names and model versions?

**Before writing documentation, ask:**
- Can this be explained in 3 bullet points instead of 3 paragraphs?
- Does this belong in main README or does it need a separate file?
- Am I explaining something obvious that the code already shows?
- Can I replace prose with a working code example?

**When working with Jupyter notebooks, ask:**
- Have I WebSearched for latest API docs for all external APIs used?
- Have I executed the entire notebook end-to-end?
- Have I fixed all deprecated parameters and methods?
- Are all outputs visible in the executed version?
- Have I documented API changes discovered?

**Before committing changes, ask:**
- Does the feature/iteration work completely (tests pass, code runs)?
- Did I update all related files (code, docs, configs)?
- Is my commit message descriptive of what was accomplished?
- Am I ready to start the next feature from this state?
- Did I verify with grep that changes are complete?
