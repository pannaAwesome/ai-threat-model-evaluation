graph TD
    root["Compromise Cloud Application"]
    auth["Gain Unauthorized Access"]
    root --> auth
    auth1["Exploit Basic Authentication Vulnerabilities"]
    auth --> auth1
    auth2["Session Hijacking"]
    auth --> auth2
    auth2_1["Steal Session ID"]
    auth2 --> auth2_1
    auth2_2["Predict Session ID"]
    auth2 --> auth2_2
    data["Compromise Data Integrity"]
    root --> data
    data1["Intercept Data Transfer"]
    data --> data1
    data1_1["Break HTTPS/SSL/TLS Encryption"]
    data1 --> data1_1
    data2["Inject Malicious XML"]
    data --> data2
    data2_1["Exploit XML Parsing Vulnerabilities"]
    data2 --> data2_1
    service["Compromise Web Service"]
    root --> service
    service1["Exploit Java Web Container Vulnerabilities"]
    service --> service1
    service2["Compromise EC2 Instance"]
    service --> service2
    service2_1["Gain Unauthorized Access to EC2"]
    service2 --> service2_1
    ui["Compromise Web UI"]
    root --> ui
    ui1["Exploit JQuery Vulnerabilities"]
    ui --> ui1
    ui2["Phishing Attack"]
    ui --> ui2
    ui2_1["Trick User into Revealing Credentials"]
    ui2 --> ui2_1
    db["Compromise PostgreSQL Database"]
    root --> db
    db1["Exploit RDS Vulnerabilities"]
    db --> db1
    db2["SQL Injection"]
    db --> db2
    db2_1["Inject Malicious SQL Queries"]
    db2 --> db2_1