import { Task, User, CreateTaskData, UpdateTaskData } from "@/lib/types";
import { authClient } from "./auth-client";

// Base API configuration
const API_BASE_URL = (
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"
).replace("localhost", "127.0.0.1");
console.log("🔧 API Client initialized with base URL:", API_BASE_URL);
// Updated: 2026-01-02 - Port fixed to 8000 to match backend terminal

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
        console.warn("Unauthorized access - Session may have expired");
        // Optional: Clear tokens here if they are stored in localStorage
        if (typeof window !== "undefined") {
          localStorage.removeItem("auth_token");
          localStorage.removeItem("user_id");
        }
        return []; // Return empty list to prevent UI crash
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || "Failed to fetch tasks");
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
        if (typeof window !== "undefined") {
          localStorage.removeItem("auth_token");
          localStorage.removeItem("user_id");
        }
        throw new Error("Session expired - please sign in again");
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || "Failed to create task");
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
        if (typeof window !== "undefined") {
          localStorage.removeItem("auth_token");
          localStorage.removeItem("user_id");
        }
        throw new Error("Session expired - please sign in again");
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || "Failed to update task");
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
        if (typeof window !== "undefined") {
          localStorage.removeItem("auth_token");
          localStorage.removeItem("user_id");
        }
        throw new Error("Session expired - please sign in again");
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || "Failed to delete task");
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
        if (typeof window !== "undefined") {
          localStorage.removeItem("auth_token");
          localStorage.removeItem("user_id");
        }
        throw new Error("Session expired - please sign in again");
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || "Failed to toggle task");
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
      const url = `${API_BASE_URL}/api/admin/users`;
      console.log("📡 Fetching users from:", url);
      console.log("📋 Request headers:", Object.keys(headers));

      const response = await fetch(url, {
        method: "GET",
        headers: headers,
        cache: "no-store",
      });

      console.log("✅ Response status:", response.status, response.statusText);

      if (response.status === 401) {
        console.error("❌ Unauthorized - token may be invalid");
        if (typeof window !== "undefined") {
          localStorage.removeItem("auth_token");
          localStorage.removeItem("user_id");
        }
        throw new Error("Session expired - please sign in again");
      }

      if (!response.ok) {
        const errorText = await response.text();
        console.error("❌ API Error:", response.status, errorText);
        throw new Error(
          `Failed to fetch users: ${response.status} ${response.statusText}`
        );
      }

      const data = await response.json();
      console.log("📦 Received users:", data);
      return Array.isArray(data) ? data : [];
    } catch (error) {
      console.error("❌ Error fetching users:", error);
      if (error instanceof TypeError && error.message === "Failed to fetch") {
        console.error(
          `🔌 Connection failed! Is the backend running on ${API_BASE_URL}?`
        );
      }
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
        if (typeof window !== "undefined") {
          localStorage.removeItem("auth_token");
          localStorage.removeItem("user_id");
        }
        throw new Error("Session expired - please sign in again");
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
  // Send a chat message
  async sendChatMessage(
    message: string
  ): Promise<{ success: boolean; response: string; user_message: string }> {
    try {
      const headers = await this.getAuthHeaders();
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: "POST",
        headers: headers,
        body: JSON.stringify({ message }),
      });

      if (response.status === 401) {
        if (typeof window !== "undefined") {
          localStorage.removeItem("auth_token");
          localStorage.removeItem("user_id");
        }
        throw new Error("Session expired - please sign in again");
      }

      if (!response.ok) {
        throw new Error(
          `Failed to send message: ${response.status} ${response.statusText}`
        );
      }

      return await response.json();
    } catch (error) {
      console.error("Error sending chat message:", error);
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
export const sendChatMessage = (message: string) =>
  apiClient.sendChatMessage(message);
