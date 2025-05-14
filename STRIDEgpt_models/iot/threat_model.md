## Threat Model

| Threat Type | Scenario | Potential Impact |
|-------------|----------|------------------|
| Spoofing | An attacker could spoof the Browser's identity to gain access to the IoT Edge device over the same network, as Basic Authentication is being used. | Unauthorized access to sensitive data and control over the IoT Edge device. |
| Spoofing | An attacker impersonates the IoT Edge Device to send malicious data to Azure services by intercepting and modifying network traffic. | Compromised integrity of telemetry data and potential denial of legitimate services. |
| Spoofing | An attacker spoofs the identity of M1 to interact with M2 and M3, leading to unauthorized access to internal communications. | Potential manipulation of live video streams and order scanning results. |
| Tampering | An attacker intercepts and modifies the data sent from M3 to the Azure Cognitive Service, altering OCR and Text-to-Speech information. | Incorrect translations and audio outputs, leading to misinformation and potential operational disruptions. |
| Tampering | An attacker modifies the telemetry information sent from the IoT Edge Device to Azure Application Insights. | False analytics and monitoring data, leading to incorrect operational decisions. |
| Tampering | An attacker tampers with the connection strings stored in GitHub secrets, leading to unauthorized access to Azure services. | Unauthorized access to sensitive data and potential service disruptions. |
| Repudiation | An attacker performs malicious actions and denies their involvement due to the lack of robust logging and auditing mechanisms. | Difficulty in identifying the source of attacks and holding attackers accountable. |
| Repudiation | An attacker manipulates the telemetry data sent to Azure Application Insights, making it difficult to trace back the source of data manipulation. | Loss of trust in the telemetry data and inability to identify the source of malicious activities. |
| Repudiation | An attacker denies performing unauthorized actions on the IoT Edge Device due to weak logging mechanisms on the device. | Difficulty in tracing back unauthorized actions to the attacker. |
| Information Disclosure | An attacker intercepts the connection strings used by Azure services, leading to unauthorized access to sensitive data. | Compromised sensitive data and potential misuse of Azure services. |
| Information Disclosure | An attacker accesses the video frames processed by M1, M2, and M3, leading to unauthorized access to sensitive video data. | Compromised privacy and potential misuse of sensitive video data. |
| Information Disclosure | An attacker intercepts the telemetry data sent to Azure Application Insights, leading to unauthorized access to operational data. | Compromised operational data and potential misuse of telemetry information. |
| Denial of Service | An attacker floods the HTTP endpoints of M1, M2, and M3 with excessive requests, leading to a denial of service. | Interruption of video processing and telemetry data collection. |
| Denial of Service | An attacker floods the Azure Cognitive Service with excessive requests, leading to a denial of service. | Interruption of OCR and Text-to-Speech services. |
| Denial of Service | An attacker floods the Azure Storage with excessive upload requests, leading to a denial of service. | Interruption of data storage and retrieval services. |
| Elevation of Privilege | An attacker exploits vulnerabilities in the IoT Edge Device to gain elevated privileges, leading to unauthorized access to sensitive data and control over the device. | Compromised integrity and confidentiality of the IoT Edge Device. |
| Elevation of Privilege | An attacker exploits vulnerabilities in the Azure services to gain elevated privileges, leading to unauthorized access to sensitive data and control over the services. | Compromised integrity and confidentiality of Azure services. |
| Elevation of Privilege | An attacker exploits vulnerabilities in the Browser to gain elevated privileges, leading to unauthorized access to the IoT Edge Device. | Compromised integrity and confidentiality of the IoT Edge Device. |


## Improvement Suggestions

- Please provide more details about the authentication flow between components to better analyze potential authentication bypass scenarios.
- Consider adding information about how sensitive data is stored and transmitted to enable more precise data exposure threat analysis.
- Describe the network configurations and security measures in place for the public access LAN used by the IoT Edge Modules.
- Clarify the data flow between the IoT Edge Device and Azure services, including any encryption methods used.
- Provide details on the logging and auditing mechanisms in place for both the IoT Edge Device and Azure services to better analyze repudiation threats.
- Specify the trust boundaries and how data is secured across different components and services.
- Detail the security measures in place for the USB Video Camera and how it interacts with M3.
- Explain how the connection strings and other secrets are secured during deployment and runtime, including any encryption or obfuscation techniques used.
