# Frontend Development Guidelines

## Next.js 16+ with App Router

This project uses Next.js 16+ with the App Router. Follow these guidelines for frontend development:

### Core Principles
- Use Server Components by default
- Use Server Actions for mutations
- Strictly Type all props
- Leverage React Compiler for performance optimization

### Component Architecture
- Server Components: Use for data fetching and rendering when possible
- Client Components: Use only when client-side interactivity is required
- Component Composition: Build reusable UI components with clear interfaces

### Data Fetching
- Use `async`/`await` in Server Components for data fetching
- Implement proper loading and error states
- Use React Suspense for loading boundaries

### State Management
- Use Server Actions for form submissions and mutations
- Use React state for client-side UI interactions
- Implement proper error handling and validation

### Styling
- Use Tailwind CSS for styling
- Follow the utility-first approach
- Create reusable component classes

### TypeScript Usage
- Strictly type all props and return values
- Use TypeScript interfaces for complex data structures
- Implement proper type checking in all components

### Performance Optimization
- Leverage React Compiler optimizations
- Use React.memo for expensive components when necessary
- Implement proper code splitting with dynamic imports