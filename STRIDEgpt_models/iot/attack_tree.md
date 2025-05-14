graph TD
    root["Compromise Application"]
    auth["Gain Unauthorized Access"]
    root --> auth
    auth1["Exploit Basic Authentication Vulnerabilities"]
    auth --> auth1
    auth2["Compromise Connection Strings"]
    auth --> auth2
    auth2_1["Access GitHub Secrets"]
    auth2 --> auth2_1
    auth2_2["Intercept Network Traffic"]
    auth2 --> auth2_2
    data["Access Sensitive Data"]
    root --> data
    data1["Exfiltrate Data from Azure Blob Storage"]
    data --> data1
    data2["Intercept Data from IoTEdge Modules"]
    data --> data2
    data2_1["Compromise M1 Module"]
    data2 --> data2_1
    data2_2["Compromise M2 Module"]
    data2 --> data2_2
    data2_3["Compromise M3 Module"]
    data2 --> data2_3
    data2_4["Compromise IoTEdgeMetricsCollector Module"]
    data2 --> data2_4
    data3["Exfiltrate Data from Azure Cognitive Service"]
    data --> data3
    data4["Exfiltrate Data from Application Insights"]
    data --> data4
    network["Compromise Network Communication"]
    root --> network
    network1["Intercept WebSocket Communication between M1, M2, and M3"]
    network --> network1
    network2["Intercept HTTP Communication to Azure Services"]
    network --> network2
    network3["Intercept Communication between Browser and M1"]
    network --> network3
    network4["Intercept Communication between USB Video Camera and M3"]
    network --> network4
    device["Compromise IoT Edge Device"]
    root --> device
    device1["Exploit Vulnerabilities in EdgeRuntime"]
    device --> device1
    device2["Physical Tampering of IoT Edge Device"]
    device --> device2
    azure["Compromise Azure Services"]
    root --> azure
    azure1["Exploit Vulnerabilities in Azure IoT Hub"]
    azure --> azure1
    azure2["Exploit Vulnerabilities in Azure Cognitive Service"]
    azure --> azure2
    azure3["Exploit Vulnerabilities in Azure Application Insights"]
    azure --> azure3
    azure4["Exploit Vulnerabilities in Azure Storage"]
    azure --> azure4