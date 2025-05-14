CATEGORY_PROMPT = """
    You are an impartial judge evaluating whether this threat has a valid category.
    The valid categories are:
    - Spoofing
    - Tampering
    - Repudiation
    - Information Disclosure
    - Denial of Service
    - Elevation of Privilege
    
    You should disregard big and small letters.
    
    [Threat]
    {tm}
    
    [Answer Options]
    Option 1: {{ "answer": 0 }}
    Option 2: {{ "answer": 1 }}
    
    output: 
"""

ASSET_PROMPT = """
    You are an impartial judge evaluating whether this threat only addresses allowed assets.
    The allowed assets are: {assets}
    
    A threat only addresses allowed assets if:
    - The `Asset` field if present should be a valid asset
    - If the `Threat` defines the target or entry point as a valid asset, typically these are capitalized
    - If the `Mitigation` suggest to apply changes to a valid asset, typically these are capitalized    
    
    [Threat]
    {tm}
    
    output: {{ "answer": <1 for valid assets or 0 for invalid assets> }}
"""

THREAT_PROMPT = """
    You are an impartial judge evaluating whether the following two threats describe the same issue.

    Criteria:
    - The `Category` must be the same.
    - If both threats specify an `Asset`, they must match. If not, infer the asset from the `Threat` field (usually the target or entry point and capitalized).
    - The `Threat` descriptions must have the same malicious objective and impact, either stated or implied.
    - Ignore differences in style, grammar, or formatting.

    Here are examples of similar threats:

    ---

    Example 1:
    Threat A:
    {{
    "Category": "Elevation of Privilege",
    "Asset": "System",
    "Threat": "Attackers may exploit improperly implemented input validation mechanisms, and thereby gain unauthorized access to the system."
    }}

    Threat B:
    {{
    "Category": "Elevation of Privilege",
    "Asset": "System",
    "Threat": "A malicious user performs an SQL injection and they gain unauthorized access to the system."
    }}

    Output:
    {{ "answer": 1 }}

    ---

    Example 2:
    Threat A:
    {{
    "Category": "Denial of Service",
    "Asset": "System",
    "Threat": "The system is flooded with requests, overwhelming system resources and rendering it unresponsive."
    }}

    Threat B:
    {{
    "Category": "Denial of Service",
    "Threat": "An attacker performs a Denial of Service attack on the system."
    }}

    Output:
    {{ "answer": 1 }}

    ---

    Example 2:
    Threat A:
    {{
    "Category": "Spoofing",
    "Asset": "System",
    "Threat": "The system is flooded with requests, overwhelming system resources and rendering it unresponsive."
    }}

    Threat B:
    {{
    "Category": "Denial of Service",
    "Threat": "An attacker performs a Denial of Service attack on the system."
    }}

    Output:
    {{ "answer": 0 }}

    ---

    Now evaluate:

    Threat A:
    {tm1}

    Threat B:
    {tm2}

    Output: {{ "answer": <1 or 0>}}
"""

MITIGATION_PROMPT = """
    You are an impartial judge evaluating whether the following two mitigations suggest the same underlying method.

    Criteria:
    - The `Mitigation` field must describe the same or overlapping method(s).
    - A partial overlap is acceptable — not all techniques need to be listed in both.
    - Ignore differences in wording, formatting, or technical phrasing.

    Here are examples of similar mitigations:

    ---

    Example 1:
    Mitigation A:
    {{
        "Mitigation": "Implement strict input validation on all user-supplied data to prevent injection attacks like SQL and XSS."
    }}

    Mitigation B:
    {{
        "Mitigation": "Sanitize user input before applying it anywhere in the system, and use an allowlist if possible."
    }}

    Output:
    {{ "answer": 1 }}

    ---

    Example 2:
    Mitigation A:
    {{
        "Mitigation": "Restrict access rights using the principle of least privilege."
    }}

    Mitigation B:
    {{
        "Mitigation": "Implement a mechanism that ensures that a user only has the capabilities they actually need."
    }}

    Output:
    {{ "answer": 1 }}

    ---

    Example 3:
    Mitigation A:
    {{
        "Mitigation": "Enforce MFA for all users to prevent unauthorized access to possibly sensitive data."
    }}

    Mitigation B:
    {{
        "Mitigation": "Encrypt the database to limit chance of leaking senitive data"
    }}

    Output:
    {{ "answer": 0 }}

    ---

    Now evaluate:

    Mitigation A:
    {tm1}

    Mitigation B:
    {tm2}

    Output: {{ "answer": <1 or 0>}}
"""

RISK_PROMPT = """
    You are an impartial judge evaluating the severity of risks in two elements in a tuple.

    Criteria:
    - The risk present the same level of severity, regardless of the format.
    - Ignore any difference in style, grammar, or punctuation.

    Here are examples of risks that present the same level of severity:

    ---

    Example 1:
    Risk A:
    {{"Risk": "High Risk"}}

    Risk B:
    {{"Risk": "3 out of 3"}}

    Output:
    {{ "answer": 0 }}

    ---

    Example 2:
    Risk A:
    {{"Risk": "Medium Risk"}}

    Risk B:
    {{"Risk": "50 out of 100"}}

    Output:
    {{ "answer": 0 }}

    ---

    Example 3:
    Risk A:
    {{"Risk": "Low Risk"}}

    Risk B:
    {{"Risk": "3 out of 10"}}

    Output:
    {{ "answer": 0 }}

    ---

    Here are examples where the risk in Risk B is lower than in Risk A:

    ---

    Example 4:
    Risk A:
    {{"Risk": "High Risk"}}

    Risk B:
    {{"Risk": "2 out of 3"}}

    Output:
    {{ "answer": -1 }}

    ---

    Example 5:
    Risk A:
    {{"Risk": "Medium Risk"}}

    Risk B:
    {{"Risk": "10 out of 100"}}

    Output:
    {{ "answer": -1 }}

    ---

    Example 6:
    Risk A:
    {{"Risk": "Low Risk"}}

    Risk B:
    {{"Risk": "2 out of 10"}}

    Output:
    {{ "answer": -1 }}

    ---

    Here are examples where the risk in Risk B is higher than in Risk A:

    ---

    Example 7:
    Risk A:
    {{"Risk": "Medium Risk"}}

    Risk B:
    {{"Risk": "79 out of 100"}}

    Output:
    {{ "answer": 1 }}

    ---

    Example 8:
    Risk A:
    {{"Risk": "Low Risk"}}

    Risk B:
    {{"Risk": "8 out of 10"}}

    Output:
    {{ "answer": 1 }}

    ---

    Example 9:
    Risk A:
    {{"Risk": "Low Risk"}}

    Risk B:
    {{"Risk": "5 out of 10"}}

    Output:
    {{ "answer": 1 }}

    ---

    Now evaluate:

    Risk A:
    {tm1}

    Risk B:
    {tm2}

    Output: {{ "answer": <0, 1 or -1>}}
"""