from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

#create a base model for my todothat will store data
class Todo(BaseModel):
    title: str
    description: str
    done: bool 

todos = [] #hold memory of all todos

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse(content="""<!DOCTYPE html>
<html>
<head>
    <title>Todo App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background: pink;
        }
        h1 {
            color: #333;
        }
        form {
            background: #f4f4f4;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        input, textarea {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        button {
            background: #28a745;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background: #218838;
        }
        .delete-btn {
            background: gray;
            padding: 5px 15px;
            font-size: 14px;
        }
        .delete-btn:hover {
            background: #c82333;
        }
        .todo-item {
            background: white;
            padding: 15px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
            display: flex;
            align-items: start;
            gap: 10px;
        }
        .todo-item.done .todo-content {
            text-decoration: line-through;
            color: #666;
        }
        .todo-content {
            flex: 1;
        }
        input[type="checkbox"] {
            width: 20px;
            height: 20px;
            margin-top: 5px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>My Todo List</h1>
    
    <form id="todoForm">
        <h3>Add New Todo</h3>
        <input type="text" id="title" placeholder="Title" required>
        <textarea id="description" placeholder="Description" required></textarea>
        <button type="submit">Add Todo</button>
    </form>

    <h3>Your Todos:</h3>
    <div id="todoList"></div>

    <script>
        async function loadTodos() {
            const response = await fetch('/todos');
            const todos = await response.json();
            const todoList = document.getElementById('todoList');
            
            if (todos.length === 0) {
                todoList.innerHTML = '<p>No todos yet! Add one above.</p>';
            } else {
                todoList.innerHTML = todos.map((todo, index) => `
                    <div class="todo-item ${todo.done ? 'done' : ''}">
                        <input type="checkbox" ${todo.done ? 'checked' : ''} onchange="toggleTodo(${index}, this.checked)">
                        <div class="todo-content">
                            <strong>${todo.title}</strong>
                            <p>${todo.description}</p>
                        </div>
                        <button class="delete-btn" onclick="deleteTodo(${index})">Delete</button>
                    </div>
                `).join('');
            }
        }

        document.getElementById('todoForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const title = document.getElementById('title').value;
            const description = document.getElementById('description').value;
            
            const response = await fetch('/todos', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    title: title,
                    description: description,
                    done: false
                })
            });
            
            if (response.ok) {
                document.getElementById('title').value = '';
                document.getElementById('description').value = '';
                loadTodos();
            }
        });

        async function toggleTodo(index, isDone) {
            const todos = await (await fetch('/todos')).json();
            const todo = todos[index];
            
            const response = await fetch(`/todos/${index}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    title: todo.title,
                    description: todo.description,
                    done: isDone
                })
            });
            
            if (response.ok) {
                loadTodos();
            }
        }

        async function deleteTodo(index) {
            if (confirm('Are you sure you want to delete this todo?')) {
                const response = await fetch(`/todos/${index}`, {
                    method: 'DELETE'
                });
                
                if (response.ok) {
                    loadTodos();
                }
            }
        }

        loadTodos();
    </script>
</body>
</html>""")

@app.get("/todos")
def get_todos():
    return todos
#return all todos

@app.post("/todos")
def create_todo(todo: Todo):
    todos.append(todo)
    return {"message": "Todo created!", "todo": todo}

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo: Todo):
        if todo_id < 0 or  todo_id >= len(todos):
            raise HTTPException(status_code=404, detail="Todo not found")
        todos[todo_id] = todo
        return {"message": "Todo updated!", "todo": todo}
#update a todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
        if todo_id < 0 or  todo_id >= len(todos):
            raise HTTPException(status_code=404, detail="Todo not found")
        todos.pop(todo_id)
        return {"message": "Todo deleted!"}
#delete a todo

