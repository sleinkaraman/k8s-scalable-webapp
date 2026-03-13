from flask import Flask, render_template_string
import socket
import os
import signal

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>K8s Cluster Node | System Monitor</title>
    <style>
        :root {
            --primary-blue: #1a73e8;
            --border-color: #dadce0;
            --bg-color: #f8f9fa;
            --text-main: #202124;
            --text-secondary: #5f6368;
        }
        body {
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .monitor-card {
            background: white;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            width: 100%;
            max-width: 480px;
            padding: 32px;
            box-shadow: 0 1px 3px rgba(60,64,67, 0.3);
        }
        .header {
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 16px;
            margin-bottom: 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .header h2 {
            margin: 0;
            font-size: 1.25rem;
            font-weight: 500;
            color: var(--text-main);
        }
        .status-indicator {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.85rem;
            color: #188038;
            font-weight: 500;
        }
        .dot { height: 8px; width: 8px; background-color: #188038; border-radius: 50%; display: inline-block; }
        .data-row {
            margin-bottom: 20px;
        }
        .label {
            font-size: 0.75rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
        }
        .value {
            font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
            background: #f1f3f4;
            padding: 12px;
            border-radius: 4px;
            font-size: 0.95rem;
            color: var(--primary-blue);
            border: 1px solid var(--border-color);
        }
        .description {
            font-size: 0.9rem;
            color: var(--text-secondary);
            line-height: 1.5;
            margin-bottom: 24px;
        }
        .actions {
            display: flex;
            gap: 12px;
            border-top: 1px solid var(--border-color);
            padding-top: 24px;
        }
        .btn {
            font-size: 0.875rem;
            font-weight: 500;
            padding: 8px 24px;
            border-radius: 4px;
            cursor: pointer;
            transition: background 0.2s;
            text-decoration: none;
            display: inline-block;
        }
        .btn-outline {
            border: 1px solid var(--border-color);
            color: var(--primary-blue);
            background: white;
        }
        .btn-outline:hover { background: #f8f9fa; }
        .btn-danger {
            background: #d93025;
            color: white;
            border: none;
        }
        .btn-danger:hover { background: #b22a15; }
    </style>
</head>
<body>
    <div class="monitor-card">
        <div class="header">
            <h2>Cluster Node Monitor</h2>
            <div class="status-indicator">
                <span class="dot"></span> Active
            </div>
        </div>
        
        <p class="description">
            This instance is part of the <strong>k8s-scalable-webapp</strong> deployment. 
            Traffic is being managed by the Kubernetes Service Load Balancer.
        </p>

        <div class="data-row">
            <div class="label">Current Pod Hostname</div>
            <div class="value">{{ hostname }}</div>
        </div>

        <div class="actions">
            <a href="/" class="btn btn-outline">Refresh Status</a>
            <a href="/kill" class="btn btn-danger">Simulate Failure</a>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    hostname = socket.gethostname()
    return render_template_string(HTML_TEMPLATE, hostname=hostname)

@app.route('/kill')
def kill():
    os.kill(os.getpid(), signal.SIGINT)
    return "Node failure simulated. Kubernetes will re-provision."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)