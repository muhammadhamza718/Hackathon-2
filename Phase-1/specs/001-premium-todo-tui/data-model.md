# Data Model: Premium Todo TUI (Phase-1)

## Task Entity

**Description**: Represents a single todo item with all required attributes

**Fields**:
- `id`: int (auto-generated, unique identifier)
- `title`: str (required, max 50 characters)
- `description`: str (optional, max 200 characters)
- `priority`: Enum (values: "Low", "Medium", "High")
- `completed`: bool (default: False)
- `tags`: List[str] (optional, list of tag strings)
- `created_at`: datetime (timestamp of creation)

**Validation Rules**:
- `title` must be 1-50 characters
- `description` must be 0-200 characters if provided
- `priority` must be one of "Low", "Medium", "High"
- `completed` must be boolean
- `tags` must be a list of strings with reasonable limits per tag

## Filter Entity

**Description**: Represents filtering criteria that can be applied to task lists

**Fields**:
- `status`: Enum (values: "All", "Pending", "Completed")
- `priority`: Enum (values: "All", "Low", "Medium", "High")
- `tags`: List[str] (optional, filter by specific tags)

**Validation Rules**:
- `status` must be one of the defined values
- `priority` must be one of the defined values
- `tags` can be empty or contain valid tag strings

## SearchQuery Entity

**Description**: Represents a text-based search query for filtering tasks

**Fields**:
- `query`: str (search text to match against task titles and descriptions)

**Validation Rules**:
- `query` can be empty (returns all tasks) or contain search text
- Maximum reasonable length for performance considerations

## State Transitions

**Task States**:
- `Pending` (default when created)
- `Completed` (when marked complete)

**Transition Rules**:
- `Pending` → `Completed` (via toggle completion)
- `Completed` → `Pending` (via toggle completion)