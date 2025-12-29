# UI Components Specification: OriginUI Design System

## Overview
This document defines the OriginUI design system components for the task management application. All components follow the Premium/Glassmorphism aesthetic and are built using Tailwind CSS.

## Component Structure
```
frontend/components/ui/
├── button.tsx
├── input.tsx
├── label.tsx
├── dialog.tsx
├── card.tsx
├── task-card.tsx
└── admin-user-card.tsx
```

## Core Components

### Button Component
- **File**: `frontend/components/ui/button.tsx`
- **Purpose**: Primary action button with multiple variants
- **Variants**:
  - `primary`: Main call-to-action buttons (e.g., "Create Task", "Save")
  - `secondary`: Secondary actions (e.g., "Cancel", "Back")
  - `destructive`: Destructive actions (e.g., "Delete", "Remove")
  - `ghost`: Minimal styling for subtle actions
- **Styles**:
  - Glassmorphism effect with backdrop blur
  - Premium gradient backgrounds
  - Smooth hover transitions
  - Proper focus states for accessibility

### Input Component
- **File**: `frontend/components/ui/input.tsx`
- **Purpose**: Text input fields with consistent styling
- **Features**:
  - Glassmorphism aesthetic with subtle borders
  - Focus states with enhanced visibility
  - Error states with visual indicators
  - Support for different input types (text, password, etc.)
- **Styles**:
  - Semi-transparent background with backdrop blur
  - Smooth border transitions
  - Proper padding and typography

### Label Component
- **File**: `frontend/components/ui/label.tsx`
- **Purpose**: Accessible labels for form elements
- **Features**:
  - Proper htmlFor association
  - Premium typography
  - Required field indicators
- **Styles**:
  - Glassmorphism aesthetic
  - Appropriate font weights and sizes

### Dialog Component
- **File**: `frontend/components/ui/dialog.tsx`
- **Purpose**: Modal dialogs for forms and confirmations
- **Features**:
  - Overlay backdrop with blur effect
  - Centered modal content
  - Close functionality (X button and ESC key)
  - Accessible with proper ARIA attributes
- **Styles**:
  - Premium glassmorphism panel
  - Smooth open/close animations
  - Proper z-index management

## Task-Specific Components

### Task Card Component
- **File**: `frontend/components/ui/task-card.tsx`
- **Purpose**: Display individual task information with action buttons
- **Props**:
  - `title`: Task title
  - `description`: Task description
  - `status`: Task status ("pending" | "completed")
  - `onToggle`: Function to toggle task status
  - `onEdit`: Function to edit task
  - `onDelete`: Function to delete task
- **Features**:
  - Visual status indicator (checkmark for completed, circle for pending)
  - Hover effects for interactive elements
  - Action buttons (Edit, Delete, Toggle)
- **Styles**:
  - Glassmorphism card with subtle shadow
  - Premium typography
  - Consistent spacing and alignment

### Admin User Card Component
- **File**: `frontend/components/ui/admin-user-card.tsx`
- **Purpose**: Display user information in admin dashboard with expandable task list
- **Props**:
  - `user`: User object with id, email, name
  - `tasks`: Array of tasks for this user
  - `onTaskDelete`: Function to delete a specific task
- **Features**:
  - Expandable/collapsible task list
  - Horizontal layout for user rows
  - Task deletion controls
  - Visual hierarchy for user and task information
- **Styles**:
  - Premium glassmorphism styling
  - Smooth expand/collapse animations
  - Clear visual separation between users

## Design Principles

### Glassmorphism Aesthetic
- **Background**: Semi-transparent with backdrop blur
- **Border**: Subtle borders with low opacity
- **Shadow**: Soft shadows for depth
- **Color**: Sophisticated color palette with premium feel

### Responsive Design
- **Mobile First**: Components adapt from mobile to desktop
- **Touch Friendly**: Adequate touch targets for mobile devices
- **Flexible Layouts**: Grid and flexbox for responsive behavior

### Accessibility
- **ARIA Labels**: Proper accessibility attributes
- **Keyboard Navigation**: Full keyboard support
- **Focus Management**: Clear focus indicators
- **Screen Reader Support**: Semantic HTML structure

## Implementation Guidelines

### TypeScript Interfaces
All components must include proper TypeScript interfaces for props and state management.

### Tailwind CSS Classes
- Use utility classes consistently
- Apply responsive prefixes where needed
- Follow Tailwind's best practices for maintainability

### Component Composition
- Build components that can be composed together
- Maintain consistent API patterns across components
- Allow for customization through props

## Color Palette
- **Primary**: Premium blue/purple gradient
- **Background**: Semi-transparent white with blur
- **Text**: High contrast for readability
- **Status**: Green for completed, gray for pending
- **Error**: Red for destructive actions