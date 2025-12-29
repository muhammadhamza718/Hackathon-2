// Task interface
export interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
  user_id: string;
}

// User interface
export interface User {
  id: string;
  name: string;
  email: string;
  role: string;
  created_at: string;
  is_active: boolean;
}

// API Response interfaces
export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
}

// Task creation interface (without id and timestamps)
export interface CreateTaskData {
  title: string;
  description?: string;
}

// Task update interface (partial data)
export interface UpdateTaskData {
  title?: string;
  description?: string;
  completed?: boolean;
}
