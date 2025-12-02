| Feature       | Monitoring                                           | Observability                                                                 |
|---------------|-----------------------------------------------------|-------------------------------------------------------------------------------|
| Core Question | "What is happening?"                                | "Why is it happening?"                                                        |
| Approach      | Reactive; tracks known issues and predefined metrics | Proactive and investigative; analyzes outputs to understand root causes       |
| Data Used     | Predefined metrics and alerts                       | Logs, metrics, and traces (telemetry data)                                    |
| Focus         | Tracking system health and performance through alerts | Diagnosing and understanding the internal state of a system                   |
| Use Case      | Simple systems where failure modes are predictable | Complex, distributed systems like microservices where failure modes are not all known in advance |
| Goal          | To detect and alert on problems                     | To provide the context and data needed to find the root cause                 |
