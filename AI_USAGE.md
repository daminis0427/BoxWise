# AI Usage Documentation

## 1. AI Tools Used

- **ChatGPT (OpenAI):** Used as an AI assistant during the development of the BoxWise project.

## 2. Prompts Given

The following are summaries of the prompts and requests made during development:

- Help me implement a shipping box recommendation system using Django.
- Help me write the product packing and box selection logic.
- Help me display suitable shipping boxes and recommend the cheapest option.
- Help me implement a 3D visualization of products inside a shipping box.
- Help me debug and improve the Django project.
- Help me prepare the README and GitHub submission.

*Note: These are summarized topics, not a complete verbatim prompt transcript. The exported ChatGPT conversation should be included separately.*

## 3. AI Output Accepted

The following suggestions were used or adapted during development:

- Guidance for organizing the Django project.
- Suggestions for product packing and box suitability calculations.
- Suggestions for displaying recommendation results and cost comparisons.
- Guidance for implementing the 3D packing visualization.
- Documentation and GitHub workflow guidance.

## 4. AI Output Rejected or Modified

- Some suggested terminal commands were modified to work in the Windows Command Prompt.
- File locations and Git instructions were adjusted to match the actual project structure.
- Suggested code and documentation were reviewed and adapted to the existing project.

## 5. AI Mistakes and Limitations

- Some terminal commands were initially provided for PowerShell, although the project terminal was Windows Command Prompt.
- Some file-location assumptions needed correction.
- The packing algorithm is heuristic-based and does not guarantee the mathematically optimal packing arrangement.
- AI-generated code may contain errors and requires manual testing.

## 6. How the Final Code Was Verified

The following checks should be performed and their actual results recorded:

- Run `python manage.py check` to check the Django project configuration.
- Run `python manage.py test` to execute automated tests.
- Run `python manage.py runserver` and manually check the application.
- Verify product dimensions, weight restrictions, suitable box recommendations, and cost comparisons.
- Check the 3D visualization in the browser.

GitHub synchronization was verified using `git status`. The local `main` branch was up to date with `origin/main`, and the working tree was clean.

**Important:** Only mark a test as passed after actually running it. Add the real test output to `TEST_OUTPUT.md`.
