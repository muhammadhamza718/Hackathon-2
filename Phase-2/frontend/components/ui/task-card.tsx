import * as React from "react";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Task } from "@/lib/types";
import { cn } from "@/lib/utils";

interface TaskCardProps {
  task: Task;
  onToggle: (task: Task) => void;
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => void;
}

const TaskCard = ({ task, onToggle, onEdit, onDelete }: TaskCardProps) => {
  return (
    <Card
      className={cn(
        "transition-all duration-200 hover:shadow-md",
        task.completed ? "bg-green-50/30 border-green-200/50" : "bg-white/30"
      )}
    >
      <CardContent className="p-4 pt-6">
        <div className="flex items-start gap-3">
          <button
            onClick={() => onToggle(task)}
            className={cn(
              "flex h-5 w-5 shrink-0 items-center justify-center rounded-full border mt-1 transition-colors",
              task.completed
                ? "bg-green-500 border-green-500"
                : "border-gray-300 hover:border-gray-400"
            )}
          >
            {task.completed && (
              <svg
                className="h-3.5 w-3.5 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="3"
                  d="M5 13l4 4L19 7"
                ></path>
              </svg>
            )}
          </button>
          <div className="flex-1 min-w-0">
            <h3
              className={cn(
                "font-medium truncate",
                task.completed
                  ? "line-through text-muted-foreground"
                  : "text-foreground"
              )}
            >
              {task.title}
            </h3>
            {task.description && (
              <p className="text-sm text-muted-foreground mt-1 truncate">
                {task.description}
              </p>
            )}
            <p className="text-xs text-muted-foreground mt-2">
              {new Date(task.created_at).toLocaleDateString()}
            </p>
          </div>
        </div>
      </CardContent>
      <CardFooter className="flex justify-end p-4 pt-0 gap-2">
        <Button variant="ghost" size="sm" onClick={() => onEdit(task)}>
          Edit
        </Button>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => onDelete(task.id)}
          className="text-destructive hover:text-destructive"
        >
          Delete
        </Button>
      </CardFooter>
    </Card>
  );
};

export { TaskCard };
