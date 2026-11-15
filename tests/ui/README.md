# UI Test Suite

## Purpose
Automated browser tests for the Pleiades UI. They check that the dropdowns populate and cascade correctly, that selections and submissions behave as expected, and that the results of a verse traversal are displayed to the user.

## Running the Tests

From the project root, move into the UI test folder and build with Maven:

```bash
cd tests/ui
mvn clean package
```

## Organization

### Page Object
A page object consolidates the locators for the Pleiades page in one place, along with the actions for working with the dropdowns. Tests interact with the page through this object instead of using locators directly, so a change to the page does not need to be fixed across multiple tests.

### Synchronizing With the UI
Selecting a book, chapter, verse, or depth triggers a cascade in the UI, where choosing one dropdown loads the options for the next. Test code can run faster than the cascade in staging, which can cause flaky failures. To avoid this, the dropdown selections and submissions are controlled by referencing monotonic counters exposed by the UI's JavaScript. The tests wait for the relevant counter to advance before moving on, which confirms the UI has finished updating instead of relying on fixed delays.

### Degree Connection Results
The display of degree connections for a scripture is tested by mocking the response of the traversal request. This lets the tests control exactly what the UI receives and verify how it renders the results, without depending on the real API or database.

## Manual Testing

### Citations
The citations shown at the bottom of the screen are not covered by the automated tests. For now, they should be verified manually in the staging environment before a release (deployment) to production.

## Notable Areas for Improvement

### Response Schema Mismatches

- **Current Approach:** Because the traversal response is mocked, the tests always give the UI the response shape it expects. A case where the UI expects a different schema than the API actually provides is not detected.
- **Planned Enhancement:** Add a way to catch schema mismatches between the UI and the API, such as validating the mocked responses against the API's real response schema or adding a test that exercises the real API response.

### Manual Citation Check

- **Current Approach:** Verifying the citations is a manual step in staging, and nothing enforces that it gets done.
- **Planned Enhancement:** Make the manual requirement harder to forget, such as adding it to a release checklist or pull request template, or eventually automating the check.