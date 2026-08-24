# Abdullatif Ziaye — Cybersecurity & Computer Science

## Profile
Master’s student in Computer Science with a focus on developing strong foundations in systems, algorithms, and security.

I approach cybersecurity from a systems perspective — aiming to understand how software, operating systems, and networks behave under normal and adversarial conditions.

---

##  Areas of Focus
- Cybersecurity (network analysis, exploitation fundamentals, system security)
- Linux and operating systems internals
- Networking
- Algorithms & Data Structures
- Mathematical foundations for computer science (discrete math, logic, linear algebra)

---

## 📂 Repository Scope
This repository serves as a structured record of my technical development. It includes:

- Detailed writeups of security challenges and labs  
- Network analysis and traffic inspection exercises  
- Notes on low-level and system-oriented concepts  
- Documentation of tools and methodologies (nmap, tcpdump, netcat, etc.)  
- Step-by-step breakdowns of problems and solutions  

---

## 🧠 Approach
My learning process emphasizes:

- First-principles reasoning over memorization  
- Understanding system behavior rather than relying on tools  
- Reproducing and analyzing problems independently  
- Writing precise explanations to validate understanding  

---

## 🔐 Cybersecurity Work
Current focus areas include:

- Network traffic analysis and protocol behavior  
- Vulnerability analysis and exploitation basics  
- Interaction with constrained or sandboxed environments  
- Understanding how misconfigurations and design flaws lead to vulnerabilities  

Writeups and experiments are added incrementally as I progress.

---

## 🚀 Objective
To develop into a computer scientist with strong analytical and practical security skills — capable of reasoning about systems, identifying weaknesses, and building robust solutions.

---

## 📌 Note
This repository reflects ongoing learning. Each commit represents a stage in my understanding and is intentionally preserved as part of the learning process.

---

## 🛡️ ScopeGuard

ScopeGuard is a small, transparent security posture checker I built to turn common web security observations into useful next steps. It checks HTTP security headers, transport choice, and basic TLS connectivity for systems I own or have written permission to assess.

The tool is deliberately read-only. It does not exploit vulnerabilities, brute-force credentials, crawl sites, enumerate ports, bypass controls, or modify target data. Every scan requires an explicit `--i-have-authorization` confirmation.

```bash
python -m scopeguard https://example.com --i-have-authorization
python -m scopeguard https://example.com --i-have-authorization --json
```

The implementation, tests, contribution guide, and responsible-use policy are included in this repository.
