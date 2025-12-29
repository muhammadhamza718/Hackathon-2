# Quickstart Guide: Frontend Task UI Implementation

## Overview
This guide provides instructions for setting up and running the frontend task management UI with customer dashboard and hidden admin dashboard.

## Prerequisites
- Node.js 18+
- npm or yarn
- Backend API running (see backend quickstart)

## Setup Instructions

### 1. Clone and Navigate to Frontend
```bash
cd frontend
```

### 2. Install Dependencies
```bash
npm install
# or
yarn install
```

### 3. Configure Environment Variables
Create a `.env.local` file in the frontend directory:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_URL=http://localhost:8000
```

### 4. Run Development Server
```bash
npm run dev
# or
yarn dev
```

The frontend will be available at http://localhost:3000

## Key Features

### Customer Dashboard
- Accessible at `/dashboard`
- Displays user's tasks in a grid layout
- CRUD operations for tasks
- Authentication required via Better Auth

### Hidden Admin Dashboard
- Accessible only at `/admin/dashboard`
- Requires mock authentication on each visit
- Credentials: `mhamza77188@gmail.com` / `mh2468718718`
- Shows all users and their tasks

## Project Structure
```
frontend/
├── app/                    # Next.js App Router pages
│   ├── dashboard/          # Customer dashboard
│   └── admin/dashboard/    # Admin dashboard
├── components/             # React components
│   └── ui/                 # OriginUI design system
├── lib/                    # Utilities and API client
└── hooks/                  # Custom React hooks
```

## API Integration
- All API calls are made through `frontend/lib/api.ts`
- JWT tokens are automatically attached to requests
- TypeScript interfaces ensure type safety

## Development Workflow
1. Create components in `frontend/components/ui/` following OriginUI patterns
2. Implement API methods in `frontend/lib/api.ts`
3. Build pages using the created components
4. Test authentication flow
5. Verify all CRUD operations work correctly

## Troubleshooting
- If API calls fail, verify the backend is running and URL is correct in .env
- If authentication doesn't work, check Better Auth configuration
- For styling issues, ensure Tailwind CSS is properly configured