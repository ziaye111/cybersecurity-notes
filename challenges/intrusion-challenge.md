**intrusion Challenge Writeup**

🎯 Objective

The goal of this challenge was to interact with a target system, observe its behavior, and extract useful information from the available services.
The  main objective is to capture the key (a flag) during the key synchronisation phase. Fortunately, a previous key synchronisation has been captured here, but the actual synced key is outdated. The IPs within the capture file are also different to the IPs in the container environment, but your container environment contains the same host.
🌐 Step 1 — Service Discovery
Action
I began by scanning the network to identify active hosts and running services. After identifying that the target system had an HTTP service running on port 80, I used curl to interact with it directly.

```bash
curl http://10.132.27.110
```
Result
The server responded with a JSON object that already contained a flag along with a message indicating that a keyserver was operational.

Insight
This indicated that the service was directly exposing sensitive information. Instead of requiring complex exploitation, simply interacting with the HTTP endpoint was enough to retrieve the flag. This highlights the importance of carefully analyzing responses before attempting more advanced techniques.

📡 Step 2 — Traffic Observation
Action
Next, I used tcpdump to capture network traffic for a short period. The system stored the captured traffic as .pcap files in the root directory.

Bash
tcpdump -i <interface>
ls -lh /root/*.pcap
Result
Multiple .pcap files were generated, each containing captured network traffic during the observation period.

Insight
Capturing traffic allows deeper analysis of communication between systems. Even though the flag was already obtained, this step is important for understanding how data flows and for identifying any hidden or additional information that might not be immediately visible.

🔍 Analysis
This challenge demonstrated that not all security tasks require complex exploitation techniques. In some cases, simply interacting with available services and carefully observing their responses can reveal critical information.

It also reinforced the importance of using fundamental tools such as
 curl and tcpdump, as they provide direct visibility into system behavior and network communication.

🧠 What I Learned
Misconfigured services can expose sensitive data directly.

Simple tools like curl can be very powerful when used correctly.

Network traffic analysis helps in understanding system communication.

It is important to verify responses carefully before moving to complex methods.

⚠️ Notes
This challenge emphasized the importance of observation and simplicity. It is easy to overcomplicate a problem, but sometimes the solution is already visible if the system is analyzed carefully.

<img width="254" height="74" alt="Screenshot 2026-05-04 225934" src="https://github.com/user-attachments/assets/d27cffb7-afaf-4e05-9ef2-94e6e0d0c041" />
