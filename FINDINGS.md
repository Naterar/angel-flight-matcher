# Findings

## Exercise 1 — parse_mission()

| Input                     | Result                            | Class                   |
| ------------------------- | --------------------------------- | ----------------------- |
| `""`                      | Returns `None` — guard caught it  | Handled                 |
| `abc` as weight           | `ValueError`, crash at conversion | Loud failure            |
| `12345` (int, not string) | `AttributeError` at `.split()`    | Loud failure            |
| `-2` passengers           | Returned as a valid mission       | **Silent wrong answer** |
| Empty pickup airport      | Returned as a valid mission       | **Silent wrong answer** |

The guard checks field count only. It does not check that fields are
non-empty, or that values are physically possible. The two silent
cases are the higher severity — a crash announces itself; a mission
record with no departure airport does not.

Deferred to Exercise 2, where rejected rows are counted and the
rejection reason has somewhere to go.

## Exercise 2 — load_intake()

| Input            | Result                                                         | Class        |
| ---------------- | -------------------------------------------------------------- | ------------ |
| Missing file     | `FileNotFoundError`, traceback                                 | Loud failure |
| One bad row in 8 | **All 8 rows lost** — exception kills the loop before `return` | **Critical** |

A single malformed row anywhere in the file destroys every valid row
parsed before it. The function has no way to skip a bad row and
continue.
