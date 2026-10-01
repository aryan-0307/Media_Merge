# Indian Movies Dataset Preparation

## Source Information
- **Original Dataset Name**: Indian Movies dataset
- **Original Source**: Kaggle (published by Naresh Bhat)
- **Source URL**: https://www.kaggle.com/nareshbhat/indian-moviesimdb
- **Original Row Count**: 50,602
- **Original Column Count**: 8
- **Date of Preparation**: September 30, 2026

## Final Output Information
- **Final Row Count**: 50,000 (exactly as required)
- **Final Column Count**: 11
- **Output File**: `mediamerge_movies_50000.csv`

## Final Columns and Source Mapping
| Final Column | Source Column | Notes |
| :--- | :--- | :--- |
| `source_id` | `ID` | Original IMDB ID or identifier. Mapped directly, `-` replaced with empty strings. |
| `title` | `Movie Name` | Mapped directly. |
| `original_title` | `Movie Name` (Derived) | Source lacks this field; copied `title` directly. |
| `media_type` | None (Derived) | Derived classification; all set to `Movie` (dataset contains only movies). |
| `release_year` | `Year` | Extracted the 4-digit year from the mixed string (e.g., `(II 2017)` -> `2017`). |
| `runtime_minutes` | `Timing(min)` | Extracted numeric minutes. |
| `language` | `Language` | Mapped directly. |
| `genre` | `Genre` | Mapped directly. |
| `rating` | `Rating(10)` | Mapped directly. |
| `vote_count` | `Votes` | Extracted numeric values, removed commas. |
| `description` | None (Derived) | Source lacks this field; left empty/blank. |

## Cleaning & Preparation Procedures

### Duplicate Handling
- **Original exact row duplicates**: After stripping whitespace, 1 exact duplicate row was found out of 50,602 rows in the raw data.
- **Derived Format Duplicates**: When transforming the 8 columns into the final 11-column format and cleaning the year/runtime, a few additional records became identical. These were also excluded to ensure strict uniqueness.
- **Selection**: To reach exactly 50,000 rows, the dataset was sorted to prioritize rows with a valid `ID` and `Year`, and exactly the top 50,000 unique rows were selected. The remaining ~600 low-quality rows (mostly lacking IDs and years) were safely excluded.

### Missing-Value Handling
- Placeholder strings like `-` in the original dataset (especially in `ID`, `Timing(min)`, `Rating(10)`, `Genre`, and `Language`) were converted to empty strings for cleaner integration into databases.
- `Year` values missing from the source were left as empty strings.

### Derived Columns
As requested, exactly 11 columns were generated. Because the source only contained 8 columns, 3 additional columns were derived/added to reach the target format:
1. `media_type`: Explicitly derived as `Movie` to satisfy the schema requirement, since the source dataset comprises Indian Movies.
2. `original_title`: Duplicated from `title` because the source does not differentiate between local and original titles.
3. `description`: Left blank because the source lacks plot synopses or descriptions. 
*(Note: These are explicitly documented derived fields and do not fabricate misleading source data.)*

## Django & MySQL Integration

The verified CSV dataset has been successfully imported into the MediaMerge MySQL database.

**Data Flow:**
`CSV` → `MovieDatasetRecord` (Django Model) → `MySQL` (`catalog_moviedatasetrecord` table)

**Architecture Distinction:**
It is critical to distinguish between the two media-related models in this project:
- **`MovieDatasetRecord`**: The **50K metadata dataset** imported from Kaggle. This represents pure read-only metadata (a catalog of real-world movies) and does NOT contain any playable files, DRM, or access tokens.
- **`MediaAsset`**: The **actual MediaMerge streamable content**. These are the internal platform assets (with physical media files, thumbnails, publication statuses, subscriptions/royalties integration). 

The 50,000 records were efficiently bulk-inserted into the `MovieDatasetRecord` model. None of the existing demo users, subscriptions, streams, royalties, or `MediaAsset` records were modified or deleted during this process.

