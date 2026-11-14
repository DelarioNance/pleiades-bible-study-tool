# GitHub Actions Workflows

## Purpose
Automation for testing and deploying Pleiades. Each workflow file begins with a header comment describing its triggers, required secrets, and notes, so this README covers only how the workflows fit together.

## Workflows

| Workflow | Runs when | What it covers |
|----------|-----------|----------------|
| **Continuous Integration (CI)** | A pull request is opened or updated | ETL, API, and UI tests against a temporary database |
| **Continuous Delivery (CD)** | A pull request into main is merged, or manually | Rebuilds the staging database and deploys to staging |
| **Staging Tests** | CD finishes successfully | UI tests against the live staging site |
| **Production Deployment** | Manually, from the Actions tab | Rebuilds the production database and deploys to production |

## How They Fit Together

1. **Before merging:** CI validates the pull request in isolation. It starts its own Postgres container, so no real environment is touched.
2. **After merging:** CD deploys the merged code to staging.
3. **After deploying:** Staging Tests run automatically and confirm the deployed app works. A failed deployment skips this step.
4. **Releasing:** Production Deployment is a deliberate manual run, separate from the automatic staging flow.

CD and Production Deployment can both be started by hand from the Actions tab. For CD, this is useful for redeploying staging without a new merge.

## Environments

- **CI** uses a throwaway database that exists only for the duration of the run.
- **Staging** is a persistent environment on FastAPI Cloud with its own database. It is rebuilt on every deployment.
- **Production** is a persistent environment on FastAPI Cloud with its own database. It is rebuilt on every deployment, and only deployed when someone runs Production Deployment manually.

## Things to Know

- **Secrets live in repository settings.** Each workflow header lists the secrets it needs. Staging and production database values are also configured in FastAPI Cloud, so changing them means updating both places.
- **Deployments can block the app.** The ETL runs as a single transaction, so staging and production may be blocked while it is running.
- **Production deployment is manual for now.** Because the app is in its MVP stage, production is deployed by a deliberate manual run instead of automatically.