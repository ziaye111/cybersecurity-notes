# Process Management

Attackers hide in running processes. Defenders need to know how to spot anomalies, isolate them, and kill them.

## 1. Viewing Processes
- **`ps aux`**: Displays a snapshot of all currently running processes across all users.
- **`top`** or **`htop`**: Provides a real-time, dynamic view of running processes, sorted by CPU or memory usage.

## 2. Managing Processes
- **`kill <PID>`**: Sends a SIGTERM signal to gracefully stop a process.
- **`kill -9 <PID>`**: Sends a SIGKILL signal to forcefully terminate a process immediately (useful for hung or malicious processes).

## 3. Background / Foreground
- **`<command> &`**: Runs a command in the background, freeing up the terminal.
- **`jobs`**: Lists currently backgrounded jobs.
- **`fg <job_number>`**: Brings a background job back to the foreground.
