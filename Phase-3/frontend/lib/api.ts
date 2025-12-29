import { Task, User, CreateTaskData, UpdateTaskData } from "@/lib/types";
import { authClient } from "./auth-client";

// Base API configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function getAuthToken(): Promise<string | null> {
  try {
    const session = await authClient.getSession();
    return session.data?.session?.token ?? null;
  } catch (error) {
    console.error("Error getting auth token:", error);
    return null;
  }
}

async function getUserId(): Promise<string | null> {
  try {
    const session = await authClient.getSession();
    return session.data?.user?.id ?? null;
  } catch (error) {
    console.error("Error getting user ID:", error);
    return null;
  }
}

// API client with JWT token handling
class ApiClient {
  private async getAuthHeaders(): Promise<HeadersInit> {
    const token = await getAuthToken();
    console.log("DEBUG: getAuthHeaders token present?", !!token); // Debug log
    if (!token) console.warn("DEBUG: No token found in getAuthHeaders!");
    return {
      "Content-Type": "application/json",
      ...(token && { Authorization: `Bearer ${token}` }),
    };
  }

  // Get all tasks for the authenticated user
  async getTasks(): Promise<Task[]> {
    try {
      const userId = await getUserId();
      if (!userId) throw new Error("User session not found");

      const headers = await this.getAuthHeaders();
      const url = `${API_BASE_URL}/api/${userId}/tasks`.replace(
        /([^:]\/)\/+/g,
        "$1"
      );
      console.log(`DEBUG: Fetching tasks from: ${url}`);
      const response = await fetch(url, {
        method: "GET",
        headers: headers,
        cache: "no-store",
      });

      if (response.status === 401) {
        throw new Error("Unauthorized - please sign in again");
      }

      if (!response.ok) {
        throw new Error(
          `Failed to fetch tasks: ${response.status} ${response.statusText}`
        );
      }

      const data = await response.json();
      return Array.isArray(data) ? data : [];
    } catch (error) {
      console.error("Error fetching tasks:", error);
      throw error;
    }
  }

  // Create a new task
  async createTask(taskData: CreateTaskData): Promise<Task> {
    try {
      const userId = await getUserId();
      if (!userId) throw new Error("User session not found");

      const headers = await this.getAuthHeaders();
      const url = `${API_BASE_URL}/api/${userId}/tasks`.replace(
        /([^:]\/)\/+/g,
        "$1"
      );

      const response = await fetch(url, {
        method: "POST",
        headers: headers,
        body: JSON.stringify(taskData),
      });

      if (response.status === 401) {
        throw new Error("Unauthorized - please sign in again");
      }

      if (!response.ok) {
        throw new Error(
          `Failed to create task: ${response.status} ${response.statusText}`
        );
      }

      return await response.json();
    } catch (error) {
      console.error("Error creating task:", error);
      throw error;
    }
  }

  // Update an existing task
  async updateTask(taskId: string, taskData: UpdateTaskData): Promise<Task> {
    try {
      const userId = await getUserId();
      if (!userId) throw new Error("User session not found");

      const headers = await this.getAuthHeaders();
      const url = `${API_BASE_URL}/api/${userId}/tasks/${taskId}`.replace(
        /([^:]\/)\/+/g,
        "$1"
      );

      const response = await fetch(url, {
        method: "PUT",
        headers: headers,
        body: JSON.stringify(taskData),
      });

      if (response.status === 401) {
        throw new Error("Unauthorized - please sign in again");
      }

      if (!response.ok) {
        throw new Error(
          `Failed to update task: ${response.status} ${response.statusText}`
        );
      }

      return await response.json();
    } catch (error) {
      console.error("Error updating task:", error);
      throw error;
    }
  }

  // Delete a task
  async deleteTask(taskId: string): Promise<void> {
    try {
      const userId = await getUserId();
      if (!userId) throw new Error("User session not found");

      const headers = await this.getAuthHeaders();
      const url = `${API_BASE_URL}/api/${userId}/tasks/${taskId}`.replace(
        /([^:]\/)\/+/g,
        "$1"
      );

      const response = await fetch(url, {
        method: "DELETE",
        headers: headers,
      });

      if (response.status === 401) {
        throw new Error("Unauthorized - please sign in again");
      }

      if (!response.ok) {
        throw new Error(
          `Failed to delete task: ${response.status} ${response.statusText}`
        );
      }
    } catch (error) {
      console.error("Error deleting task:", error);
      throw error;
    }
  }

  // Toggle task completion status
  async toggleTask(taskId: string, completed: boolean): Promise<Task> {
    try {
      const userId = await getUserId();
      if (!userId) throw new Error("User session not found");

      const headers = await this.getAuthHeaders();
      const url =
        `${API_BASE_URL}/api/${userId}/tasks/${taskId}/complete`.replace(
          /([^:]\/)\/+/g,
          "$1"
        );

      const response = await fetch(url, {
        method: "PATCH",
        headers: headers,
        body: JSON.stringify({ completed }),
      });

      if (response.status === 401) {
        throw new Error("Unauthorized - please sign in again");
      }

      if (!response.ok) {
        throw new Error(
          `Failed to toggle task: ${response.status} ${response.statusText}`
        );
      }

      return await response.json();
    } catch (error) {
      console.error("Error toggling task:", error);
      throw error;
    }
  }

  // Get all users (admin only)
  async adminGetUsers(): Promise<User[]> {
    try {
      const headers = await this.getAuthHeaders();
      const response = await fetch(`${API_BASE_URL}/api/admin/users`, {
        method: "GET",
        headers: headers,
        cache: "no-store",
      });

      if (response.status === 401) {
        throw new Error("Unauthorized - please sign in again");
      }

      if (!response.ok) {
        throw new Error(
          `Failed to fetch users: ${response.status} ${response.statusText}`
        );
      }

      const data = await response.json();
      return Array.isArray(data) ? data : [];
    } catch (error) {
      console.error("Error fetching users:", error);
      throw error;
    }
  }

  // Get tasks for a specific user (admin only)
  async adminGetUserTasks(userId: string): Promise<Task[]> {
    try {
      const headers = await this.getAuthHeaders();
      const response = await fetch(
        `${API_BASE_URL}/api/admin/users/${userId}/tasks`,
        {
          method: "GET",
          headers: headers,
          cache: "no-store",
        }
      );

      if (response.status === 401) {
        throw new Error("Unauthorized - please sign in again");
      }

      if (!response.ok) {
        throw new Error(
          `Failed to fetch user tasks: ${response.status} ${response.statusText}`
        );
      }

      const data = await response.json();
      return Array.isArray(data) ? data : [];
    } catch (error) {
      console.error("Error fetching user tasks:", error);
      throw error;
    }
  }
  // Delete a user (admin only)
  async adminDeleteUser(userId: string): Promise<void> {
    try {
      const headers = await this.getAuthHeaders();
      const response = await fetch(
        `${API_BASE_URL}/api/admin/users/${userId}`,
        {
          method: "DELETE",
          headers: headers,
        }
      );

      if (response.status === 401) {
        throw new Error("Unauthorized - please sign in again");
      }

      if (!response.ok) {
        throw new Error(
          `Failed to delete user: ${response.status} ${response.statusText}`
        );
      }
    } catch (error) {
      console.error("Error deleting user:", error);
      throw error;
    }
  }

  // Update user role (admin only)
  async adminUpdateUserRole(userId: string, role: string): Promise<User> {
    try {
      const headers = await this.getAuthHeaders();
      const response = await fetch(
        `${API_BASE_URL}/api/admin/users/${userId}/role`,
        {
          method: "PATCH",
          headers: headers,
          body: JSON.stringify({ role }),
        }
      );

      if (response.status === 401) {
        throw new Error("Unauthorized - please sign in again");
      }

      if (!response.ok) {
        throw new Error(
          `Failed to update user role: ${response.status} ${response.statusText}`
        );
      }

      return await response.json();
    } catch (error) {
      console.error("Error updating user role:", error);
      throw error;
    }
  }

  // Delete a user's task (admin only)
  async adminDeleteTask(userId: string, taskId: string): Promise<void> {
    try {
      const headers = await this.getAuthHeaders();
      const response = await fetch(
        `${API_BASE_URL}/api/admin/users/${userId}/tasks/${taskId}`,
        {
          method: "DELETE",
          headers: headers,
        }
      );

      if (response.status === 401) {
        throw new Error("Unauthorized - please sign in again");
      }

      if (!response.ok) {
        throw new Error(
          `Failed to delete user task: ${response.status} ${response.statusText}`
        );
      }
    } catch (error) {
      console.error("Error deleting user task:", error);
      throw error;
    }
  }
}

export const apiClient = new ApiClient();

// Export individual functions for direct use
export const getTasks = () => apiClient.getTasks();
export const createTask = (taskData: CreateTaskData) =>
  apiClient.createTask(taskData);
export const updateTask = (taskId: string, taskData: UpdateTaskData) =>
  apiClient.updateTask(taskId, taskData);
export const deleteTask = (taskId: string) => apiClient.deleteTask(taskId);
export const toggleTask = (taskId: string, completed: boolean) =>
  apiClient.toggleTask(taskId, completed);
export const adminGetUsers = () => apiClient.adminGetUsers();
export const adminGetUserTasks = (userId: string) =>
  apiClient.adminGetUserTasks(userId);
export const adminDeleteUser = (userId: string) =>
  apiClient.adminDeleteUser(userId);
export const adminUpdateUserRole = (userId: string, role: string) =>
  apiClient.adminUpdateUserRole(userId, role);
export const adminDeleteTask = (userId: string, taskId: string) =>
  apiClient.adminDeleteTask(userId, taskId);
