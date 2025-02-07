from flask import Flask, jsonify, render_template
import queue
import threading
import time

app = Flask(__name__)

# Task queue and workers
task_queue = queue.Queue()
workers = ["Worker1", "Worker2", "Worker3"]
worker_status = {worker: "🟡 Waiting for Task" for worker in workers}  # ✅ Define globally

# Task dependencies
task_dependencies = {
    "Testing": ["Writing Code"],
    "Integrating with Version Control": ["Writing Code"],
    "Deploying to Production": ["Integrating with Version Control", "Testing"],
    "Monitoring Performance": ["Deploying to Production"]
}

completed_tasks = {}
pending_tasks = ["Writing Code", "Testing", "Integrating with Version Control", "Deploying to Production", "Monitoring Performance"]

SLOW_DOWN_TIME = 5  # Slow down execution for visualization

def worker(name):
    """ Worker function that picks up tasks and executes them """
    global worker_status  # ✅ Access global variable

    print(f"🔵 {name} started!")

    while True:
        time.sleep(SLOW_DOWN_TIME)

        try:
            task = task_queue.get(timeout=10)
        except queue.Empty:
            worker_status[name] = "⚪ No Tasks Left"
            print(f"⚪ {name} is done working! Exiting.")
            return  

        task_name, delay = task

        # Check if dependencies are met
        dependencies_met = all(dep in completed_tasks for dep in task_dependencies.get(task_name, []))

        if dependencies_met:
            worker_status[name] = f"🛠️ Working on {task_name}"
            print(f"🛠️ {name} is doing: {task_name} (⏳ {delay}s)")
            time.sleep(delay)  # Simulate execution
            completed_tasks[task_name] = True
            pending_tasks.remove(task_name)
            worker_status[name] = f"✅ Finished: {task_name}"
            print(f"✅ {name} finished: {task_name} 🎉\n")
        else:
            worker_status[name] = f"⏳ Waiting for {task_name}"
            print(f"⏳ {name} is waiting for dependencies: {task_name} ❌")
            task_queue.put(task)

        task_queue.task_done()

# Add tasks to queue
task_queue.put(("Writing Code", 2))
task_queue.put(("Testing", 3))
task_queue.put(("Integrating with Version Control", 1))
task_queue.put(("Deploying to Production", 4))
task_queue.put(("Monitoring Performance", 5))

# Start worker threads
threads = []
for worker_name in workers:
    t = threading.Thread(target=worker, args=(worker_name,))
    t.start()
    threads.append(t)

# ✅ Flask Routes (Now `worker_status` is defined globally)
@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/status')
def status():
    return jsonify({
        "worker_status": worker_status,
        "completed_tasks": list(completed_tasks.keys()),
        "pending_tasks": pending_tasks
    })

if __name__ == '__main__':
    app.run(debug=True)