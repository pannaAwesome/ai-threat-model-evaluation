graph TD
    root["Compromise Application"]
    auth["Gain Unauthorized Access"]
    root --> auth
    auth1["Access Web Application Directly"]
    auth --> auth1
    auth2["Access Background Worker Directly"]
    auth --> auth2
    data["Compromise Data Stores"]
    root --> data
    data1["Access Web Application Config"]
    data --> data1
    data1a["Steal Credentials for Message Queue"]
    data1 --> data1a
    data2["Access Background Worker Config"]
    data --> data2
    data2a["Steal Credentials for Database"]
    data2 --> data2a
    data3["Access Message Queue"]
    data --> data3
    data3a["Inject Malicious Messages"]
    data3 --> data3a
    data3b["Eavesdrop on Messages"]
    data3 --> data3b
    data4["Access Database"]
    data --> data4
    data4a["Exfiltrate Sensitive Data"]
    data4 --> data4a
    data4b["Inject Malicious Data"]
    data4 --> data4b
    process["Compromise Processes"]
    root --> process
    process1["Compromise Web Application"]
    process --> process1
    process1a["Inject Malicious Code"]
    process1 --> process1a
    process1b["Exploit Vulnerabilities"]
    process1 --> process1b
    process2["Compromise Background Worker"]
    process --> process2
    process2a["Inject Malicious Code"]
    process2 --> process2a
    process2b["Exploit Vulnerabilities"]
    process2 --> process2b