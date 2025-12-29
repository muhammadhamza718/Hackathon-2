# Feature Specification: Frontend Task UI (003-frontend-task-ui)

## Overview
This feature implements the frontend user interface for the task management web application. It includes both the customer dashboard for standard users and a hidden admin dashboard for administrative functions. The implementation follows modern UI/UX principles with a focus on user experience and security.

## Feature Requirements

### Goal 1: Core Project Requirements (PRIORITY - Client UI)

#### Objective
Transform console app into modern web app with intuitive user interface and seamless user experience.

#### Authentication Integration
- **Sign-in/Sign-up Pages**: Implement Better Auth integration with dedicated pages
- **JWT Token Handling**: Client must attach JWT token to `Authorization: Bearer <token>` header for ALL API requests
- **Session Management**: Secure token storage and automatic refresh when needed
- **Protected Routes**: Ensure unauthorized users cannot access dashboard pages

#### Customer Dashboard (`/dashboard`)
- **Page Title**: "My Tasks" header prominently displayed
- **Task List Display**: Grid layout of `TaskCard` components showing:
  - Task Title
  - Task Description (optional)
  - Current Status (Pending/Completed)
  - Visual indicators for task state
- **CRUD Actions**:
  - **Create Task**: Modal form with required Title field and optional Description
  - **Update Task**: Inline editing or modal form to modify task details
  - **Delete Task**: Confirmation dialog before removing task
  - **Toggle Status**: Switch to change task status between Pending/Completed
- **Responsive Design**: Mobile-first approach with responsive layouts

#### Data Fetching
- **TypeScript Interfaces**: Strictly match backend API models (`User`, `Task`)
- **API Integration**: Use dedicated API service layer for all backend communications
- **Loading States**: Display appropriate loading indicators during API calls
- **Error Handling**: Show user-friendly error messages for failed requests
- **Real-time Updates**: Reflect changes immediately in the UI after successful API calls

### Goal 2: Hidden Admin Dashboard (EXTENSION)

#### Location
- **Route**: `/admin/dashboard` (hidden URL, not linked from main interface)
- **Access**: Only accessible through direct URL entry

#### Security Logic
- **Re-Login Trigger**: Every page load to `/admin/dashboard` must open a **Login Modal/Dialog**
- **Hardcoded Credentials**: Only allow access if credentials match:
  - Email: `mhamza77188@gmail.com`
  - Password: `mh2468718718`
- **Mock Admin Authentication**: Simple credential check without backend verification
- **Session Timeout**: Admin session expires after 15 minutes of inactivity

#### Layout & Functionality
- **User Overview**: Horizontal rows displaying all users in the system
- **Expandable Task Lists**: Click to expand and view tasks for each user
- **Managerial Capabilities**:
  - Delete specific user's tasks
  - View task details
  - Filter tasks by status
- **Admin Controls**: Administrative functions with appropriate UI controls

## Design System & Technical Constraints

### Tech Stack Requirements
- **Framework**: Next.js 16+ with App Router
- **Language**: TypeScript for type safety
- **Styling**: Tailwind CSS for utility-first styling approach
- **Component Architecture**: Follow shadcn/OriginUI pattern in `frontend/components/ui/`

### Implementation Rules
- **No Generic UI Libraries**: Do not use generic UI libraries like Material UI or Chakra UI
- **OriginUI Foundation**: Use provided OriginUI code (Button, Input, Label, Dialog) as foundational design system
- **Premium Aesthetic**: Styles must match "Premium/Glassmorphism" aesthetic defined in previous phases
- **Component Reusability**: Create reusable components following best practices

### Component Specifications
- **TaskCard**: Display task information with action buttons
- **Modal/Dialog**: For creating/updating tasks and admin login
- **Input Components**: Styled according to OriginUI guidelines
- **Button Components**: Consistent styling with appropriate states
- **Layout Components**: Responsive grid and flexbox layouts

## User Interface Requirements

### Customer Dashboard UI
- **Header**: Clear navigation and user profile section
- **Task Grid**: Responsive grid layout with consistent spacing
- **Empty State**: Friendly message when no tasks exist
- **Pagination/Infinite Scroll**: For handling large numbers of tasks
- **Search/Filter**: Ability to filter tasks by status or search by title

### Admin Dashboard UI
- **User List**: Horizontal scrollable list of users with basic info
- **Task Expansion**: Smooth animation when expanding user tasks
- **Admin Controls**: Clear visual distinction for administrative actions
- **Security Overlay**: Login modal that prevents access until authenticated

## API Integration Requirements
- **Strict TypeScript Interfaces**: Match backend API contracts exactly
- **Authorization Headers**: Include JWT token in all authenticated requests
- **Error Handling**: Consistent error responses from backend API
- **Loading States**: Provide feedback during API operations

## Success Criteria
- [ ] Customer dashboard displays tasks with proper UI components
- [ ] All CRUD operations work correctly with backend API
- [ ] Authentication integration functions properly
- [ ] Admin dashboard is accessible only with correct credentials
- [ ] UI follows Premium/Glassmorphism aesthetic
- [ ] TypeScript interfaces match backend API contracts
- [ ] Responsive design works across device sizes
- [ ] All OriginUI components are properly implemented

## Out of Scope
- Advanced admin features beyond the specified requirements
- Real-time notifications or WebSocket integration
- File attachments or complex task relationships
- Advanced reporting or analytics features

## Dependencies
- Better Auth for authentication
- Backend API endpoints for task management
- OriginUI component library for UI elements
- Tailwind CSS for styling