# Scoring Methodology

How each signal is scored and weighted.

## Signals

### Name (25%)

Measures keyword overlap between the repo name and the target search query. Hyphens and underscores are treated as word separators.

| Match | Score |
|-------|-------|
| All query words in name | 100 |
| Partial match | Proportional |
| No match | 0 |

### Description (15%)

Checks the About/description field length.

| Length | Score |
|--------|-------|
| Empty | 0 |
| Under 20 chars | 30 |
| 20-49 chars | 60 |
| 50-300 chars | 100 |
| Over 300 chars | 80 |

### Topics (15%)

Counts the number of topic tags.

| Count | Score |
|-------|-------|
| 0 | 0 |
| 1-4 | 40 |
| 5-9 | 70 |
| 10-20 | 100 |

### README (15%)

Based on total word count. The first 200 words matter most for GitHub search snippets.

| Words | Score |
|-------|-------|
| 0 | 0 |
| Under 50 | 20 |
| 50-199 | 50 |
| 200-499 | 75 |
| 500+ | 100 |

### Stars (20%)

Logarithmic scale reflecting competitive positioning.

| Stars | Score |
|-------|-------|
| 0 | 0 |
| 1-9 | 15 |
| 10-49 | 30 |
| 50-99 | 50 |
| 100-499 | 70 |
| 500-999 | 85 |
| 1000+ | 100 |

### Activity (10%)

Days since last push.

| Days | Score |
|------|-------|
| 0-7 | 100 |
| 8-30 | 85 |
| 31-90 | 60 |
| 91-180 | 35 |
| 180+ | 10 |

## Overall Grade

Weighted sum of all signals.

| Grade | Score |
|-------|-------|
| A | 85-100 |
| B | 70-84 |
| C | 50-69 |
| D | 30-49 |
| F | 0-29 |
