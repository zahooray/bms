# Postman collection

`collections/bms.postman_collection.json` - 17 requests covering every
endpoint in Phases 3 and 4, plus the validation failures worth seeing.

## Import

Postman -> Import -> select the file. Or, if the workspace in
`.postman/resources.yaml` is linked, it appears under Local View.

## Run order

Session authentication needs two requests before anything else:

1. `Auth / 1. Get CSRF cookie`  - GET, stores `csrftoken`
2. `Auth / 2. Login`            - POST, stores `sessionid`

Postman then sends both cookies automatically. `/api/banks/` is public
and works without them; everything under `/api/accounts/` returns 401
until you have logged in.

## Variables

| Variable     | Default                 | Notes                                   |
|--------------|-------------------------|-----------------------------------------|
| `base_url`   | `http://localhost:8000` |                                         |
| `username`   | `admin`                 |                                         |
| `password`   | `admin123`              | from `manage.py seed_superuser`         |
| `csrftoken`  | set by request 1        |                                         |
| `bank_id`    | set by `Create bank`    |                                         |
| `branch_id`  | **set this yourself**   | create a BankBranch in `/admin/` first  |
| `account_id` | set by `Create account` |                                         |

`branch_id` is the only one you fill in by hand - there is no branch API
yet, so create one through the Django admin and paste its id.

## What the failure cases demonstrate

| Request                          | Shows                                            |
|----------------------------------|--------------------------------------------------|
| Create bank - invalid SWIFT      | `validate_swift_code()`, a per-field validator    |
| Create bank - future date        | `validate()`, the cross-field hook                |
| Create account - savings < 500   | a rule needing two fields at once                 |
| List accounts - unauthenticated  | 401 JSON rather than an HTML redirect             |
| Delete bank (with accounts)      | `perform_destroy()` guarding a PROTECTed FK       |

## Note on auth

This is session auth, which is awkward from an API client - hence the
CSRF dance. Phase 5 adds `POST /api/auth/login/` returning a token, and
the collection should switch to an `Authorization: Token ...` header
then.
