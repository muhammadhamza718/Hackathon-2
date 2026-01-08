import React from 'react';
import './TodoList.css'; // We'll create this CSS file

const TodoList = ({ todos, showHeader = true }) => {
  if (!todos || todos.length === 0) {
    return (
      <div className="todo-list-container">
        {showHeader && <h3>Your Todos</h3>}
        <p className="no-todos-message">No todos found.</p>
      </div>
    );
  }

  return (
    <div className="todo-list-container">
      {showHeader && <h3>Your Todos</h3>}
      <ul className="todo-items-list">
        {todos.map((todo) => (
          <li key={todo.id} className={`todo-item ${todo.completed ? 'completed' : ''}`}>
            <div className="todo-content">
              <span className={`todo-text ${todo.completed ? 'completed' : ''}`}>
                {todo.content}
              </span>
              {todo.due_date && (
                <span className="todo-due-date">
                  Due: {new Date(todo.due_date).toLocaleDateString()}
                </span>
              )}
            </div>
            <span className={`todo-status ${todo.completed ? 'completed' : 'pending'}`}>
              {todo.completed ? '✓ Completed' : '○ Pending'}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TodoList;