# Ember Glow FW

### A firewall rule governance and compliance tool.

Ember Glow FW is a web-based firewall management tool that helps organizations track rules from request, approval, implementation and audit. An example would be to track PCI compliance.

<b>Current Main Features:</b>
* REST API first design
* Django front end
* Redis backend
* Firewall communication via REST APIs
* Plug-in system for firewalls (Anyone can integrate their firewall implementation)
* Unique rule UUIDs are used to track rules on firewalls

<b>Future Features:</b>
* Local and SSO authentication
* Rule sync to ensure compliance
* Pretty reports

<b>Flow for rules:</b>

![Flow](diagrams/Ember%20Glow%20FW%20Flow.png)

<b>Design Components</b>

![Design](diagrams/Ember%20Glow%20FW%20Componets.png)