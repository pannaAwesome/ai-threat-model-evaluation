CATEGORY_PROMPT = """
    [Task Description]
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
    Valid: {{ "answer": 0 }}
    Invalid: {{ "answer": 1 }}
    
    output: 
"""

ASSET_PROMPT = """
    [Task Description]
    You are an impartial judge evaluating whether this threat only addresses allowed assets.
    The valid assets are: {assets}
    A threat only addresses allowed assets if:
    - The `Asset` field if present should be a valid asset
    - If the `Threat` defines the target or entry point as a valid asset, typically these are capitalized
    - If the `Mitigation` suggest to apply changes to a valid asset, typically these are capitalized    
    
    [Threat]
    {tm}
    
    [Answer Options]
    Valid: {{ "answer": 0 }}
    Invalid: {{ "answer": 1 }}
    
    output:
"""

THREAT_PROMPT = """
    [Task Description]
    You are an impartial judge evaluating whether the following two threats describe the same issue.
    A Threat A and B are similar if:
    - The `Category` is the same.
    - If both threats specify an `Asset`, they must match. If not, infer the asset from the `Threat` field (usually the target or entry point and capitalized).
    - The `Threat` descriptions must have the same malicious objective and impact, either stated or implied.
    - Ignore differences in style, grammar, or formatting.

    [Examples Begin]
    [Example 1]
    Threat A:
    {{
    "Category": "Denial of Service",
    "Asset": "System",
    "Threat": "The System is flooded with requests, overwhelming system resources and rendering it unresponsive."
    }}

    Threat B:
    {{
    "Category": "Denial of Service",
    "Asset": "System"
    "Threat": "An attacker performs a Denial of Service attack on the system."
    }}

    output:
    {{ "answer": 1 }}

    [Example 2]
    Threat A:
    {{
    "Category": "Spoofing",
    "Asset": "System",
    "Threat": "The System is flooded with requests, overwhelming system resources and rendering it unresponsive."
    }}

    Threat B:
    {{
    "Category": "Denial of Service",
    "Threat": "An attacker performs a Denial of Service attack on the system."
    }}

    output:
    {{ "answer": 0 }}
    [Examples End]

    [Threat A]
    {tm1}

    [Threat B]
    {tm2}
    
    [Answer Options]
    Similar: {{ "answer": 1 }}
    Not similar: {{ "answer": 0 }}

    output: 
"""

MITIGATION_PROMPT = """
    [Task Description]
    You are an impartial judge evaluating whether the following two mitigations suggest the same underlying method.
    A Mitigation A and B are the similar if:
    - The `Mitigation` field describe the same or overlapping method(s).
    - A partial overlap is acceptable — not all techniques need to be listed in both.
    - Ignore differences in wording, formatting, or technical phrasing.

    [Examples Begin]
    [Example 1]
    Mitigation A:
    {{
        "Mitigation": "Restrict access rights using the principle of least privilege."
    }}

    Mitigation B:
    {{
        "Mitigation": "Implement a mechanism that ensures that a user only has the capabilities they actually need."
    }}

    output:
    {{ "answer": 1 }}

    [Example 2]
    Mitigation A:
    {{
        "Mitigation": "Enforce MFA for all users to prevent unauthorized access to possibly sensitive data."
    }}

    Mitigation B:
    {{
        "Mitigation": "Encrypt the database to limit chance of leaking senitive data"
    }}

    output:
    {{ "answer": 0 }}
    [Examples End]
    
    [Mitigation A]
    {tm1}

    [Mitigation B]
    {tm2}
    
    [Answer Options]
    Similar: {{ "answer": 1 }}
    Not similar: {{ "answer": 0 }}

    output: 
"""

RISK_PROMPT = """
    [Task Description]
    You are an impartial judge evaluating the severity of risks in two elements in a tuple.
    Risk A and B are the same if:
    - The risk presents the same level of severity, regardless of the format.
    - Ignore any difference in style, grammar, or punctuation.

    [Examples Begin]
    [Example 1]
    Risk A:
    {{"Risk": "High Risk"}}

    Risk B:
    {{"Risk": "3 out of 3"}}

    output:
    {{ "answer": 0 }}

    [Example 2]
    Risk A:
    {{"Risk": "Medium Risk"}}

    Risk B:
    {{"Risk": "50 out of 100"}}

    output:
    {{ "answer": 0 }}

    [Example 3]
    Risk A:
    {{"Risk": "Low Risk"}}

    Risk B:
    {{"Risk": "3 out of 10"}}

    output:
    {{ "answer": 0 }}

    [Example 4]
    Risk A:
    {{"Risk": "High Risk"}}

    Risk B:
    {{"Risk": "2 out of 3"}}

    output:
    {{ "answer": -1 }}

    ---

    [Example 5]
    Risk A:
    {{"Risk": "Medium Risk"}}

    Risk B:
    {{"Risk": "10 out of 100"}}

    output:
    {{ "answer": -1 }}
    
    [Example 6]
    Risk A:
    {{"Risk": "Low Risk"}}

    Risk B:
    {{"Risk": "2 out of 10"}}

    output:
    {{ "answer": -1 }}
    
    [Example 7:]
    Risk A:
    {{"Risk": "Medium Risk"}}

    Risk B:
    {{"Risk": "79 out of 100"}}

    output:
    {{ "answer": 1 }}
    
    [Example 8]
    Risk A:
    {{"Risk": "Low Risk"}}

    Risk B:
    {{"Risk": "8 out of 10"}}

    output:
    {{ "answer": 1 }}

    [Example 9]
    Risk A:
    {{"Risk": "Low Risk"}}

    Risk B:
    {{"Risk": "5 out of 10"}}

    output:
    {{ "answer": 1 }}
    [Examples End]

    [Risk A]
    {tm1}

    [Risk B]
    {tm2}
    
    [Answer Options]
    Similar: {{ "answer": 0 }}
    A bigger than B: {{ "answer": -1 }}
    B bigger than A: {{ "answer": 1 }}

    output: 
"""