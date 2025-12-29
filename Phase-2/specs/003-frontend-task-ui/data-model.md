# Data Model: Frontend Task UI & Admin Dashboard

## TypeScript Interfaces

### User Interface
```typescript
interface User {
  id: string;
  email: string;
  name?: string;
  role: string;
  created_at: string; // ISO date string
}
```

### Task Interface
```typescript
interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  user_id: string;
  created_at: string; // ISO date string
  updated_at: string; // ISO date string
}
```

### API Response Interfaces

#### Task API Responses
```typescript
interface GetTasksResponse {
  tasks: Task[];
}

interface CreateTaskRequest {
  title: string;
  description?: string;
}

interface CreateTaskResponse {
  task: Task;
}

interface UpdateTaskRequest {
  title?: string;
  description?: string;
  completed?: boolean;
}

interface UpdateTaskResponse {
  task: Task;
}

interface DeleteTaskResponse {
  message: string;
}
```

#### Admin API Responses
```typescript
interface AdminGetUsersResponse {
  users: User[];
}

interface AdminGetUserTasksResponse {
  tasks: Task[];
}
```

### Component Prop Interfaces

#### Task Card Props
```typescript
interface TaskCardProps {
  task: Task;
  onToggle: (task: Task) => void;
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => void;
}
```

#### Admin User Card Props
```typescript
interface AdminUserCardProps {
  user: User;
  tasks: Task[];
  onTaskDelete: (taskId: string) => void;
}
```

#### Button Component Props
```typescript
type ButtonVariant = 'primary' | 'secondary' | 'destructive' | 'ghost';

interface ButtonProps {
  children: React.ReactNode;
  variant?: ButtonVariant;
  onClick?: () => void;
  disabled?: boolean;
  className?: string;
}
```

#### Input Component Props
```typescript
interface InputProps {
  id?: string;
  type?: string;
  value?: string;
  onChange?: (value: string) => void;
  placeholder?: string;
  label?: string;
  error?: string;
  required?: boolean;
  className?: string;
}
```

#### Dialog Component Props
```typescript
interface DialogProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
  actions?: React.ReactNode;
}
```

### API Client Configuration
```typescript
interface ApiConfig {
  baseUrl: string;
  headers: {
    'Content-Type': string;
    'Authorization': string;
  };
}
```

## Validation Rules

### Task Validation
- Title: Required, minimum 1 character, maximum 255 characters
- Description: Optional, maximum 1000 characters
- Completed: Boolean value only

### User Validation
- Email: Required, valid email format
- Name: Optional, maximum 255 characters
- Role: String value, typically 'user' or 'admin'

## State Management Interfaces

### Task State
```typescript
interface TaskState {
  tasks: Task[];
  loading: boolean;
  error: string | null;
}
```

### Admin State
```typescript
interface AdminState {
  users: User[];
  selectedUserTasks: Task[] | null;
  loading: boolean;
  error: string | null;
}
```

## API Method Signatures

### Task API Methods
```typescript
// GET /api/tasks
const getTasks: () => Promise<GetTasksResponse>;

// POST /api/tasks
const createTask: (data: CreateTaskRequest) => Promise<CreateTaskResponse>;

// PUT /api/tasks/{id}
const updateTask: (id: string, data: UpdateTaskRequest) => Promise<UpdateTaskResponse>;

// DELETE /api/tasks/{id}
const deleteTask: (id: string) => Promise<DeleteTaskResponse>;

// PATCH /api/tasks/{id}/complete
const toggleTask: (id: string) => Promise<UpdateTaskResponse>;
```

### Admin API Methods
```typescript
// GET /api/admin/users
const adminGetUsers: () => Promise<AdminGetUsersResponse>;

// GET /api/admin/users/{id}/tasks
const adminGetUserTasks: (userId: string) => Promise<AdminGetUserTasksResponse>;
```