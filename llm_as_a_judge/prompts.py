HALLUCINATIONS_PROMPT = """
    You are an impartial judge, and you will be comparing the elements of two lists.
    You need to discover if any of the elements of the list use different categories or assets than what is expected.
    You have previously been told which categories we allow, and which assets are used in the application.
    
    The category can be verified purely from looking at the 'Category' field in the dictionary.
    The assets should be verified in two ways:
    1. The 'Asset' field if present
    2. The 'Threat' field, the description will detail some assets in the system, commonly these are capitalized
       and they will be either cause of the threat or be impacted by it.
    3. The 'Mitigation' field, the description will detail some assets in the system, commonly these are
       capitalized and the description will suggest to apply some changes to fix them.
    
    You only need to find one match between the two lists, and once a match is found you should not match
    that element with any other. You should always ignore any difference in style, grammar, or punctuation.
    
    The allowed categories can be either of: Spoofing, Tampering, Repudiation, Information Disclosure,
    Denial of Service, Elevation of Privilege.
    The allowed assets are: {assets}.
    
    Some examples of assets in a threat description are:
    |              Threat Description                 |                    Assets                      |
    |-------------------------------------------------|------------------------------------------------|
    | Attackers used unsafely stored credentials in   | Credentials Store                              |
    | the Credentials Store and thereby send requests |                                                |
    | to the Web Server                               |                                                |
    |-------------------------------------------------|------------------------------------------------|
    | An attacker can intercept unecrypted messages   | Browser, Web Server                            |
    | between the Browser and Web Server, and then    |                                                |
    | have the Worker process their own messages      |                                                |
    |-------------------------------------------------|------------------------------------------------|
        
    The list is:
    [List]
    {tm}
    
    Please return (ID,category) of the elements that have different categories than expected in category_list,
    and (ID,[assets]) of the elements that have different assets than expected in asset_list. If no elements are
    found then return empty lists.
    
    Once you have completed the task, please end your response with this JSON object:
    {{
        "categories": [("ID", category),...],
        "assets": [("ID", [assets]),...]
    }}
"""

THREAT_PROMPT = """
    You are an impartial judge, and you will be comparing the elements of two lists.
    You need to discover the elements in the two lists that are similar based on the following criteria:
    - The category of the threats are the same.
    - If asset is specified for both threats, then they should be the same. Otherwise,
      you can defer the asset based on the threat description, the asset would be the entry point
      of the attack.
    - The threats have the same malicious objective and impact, the impact might not be explicitly stated
      in the threat description, but it can be inferred from the context.
    - The threats may be worded differently, use abbreviations or have different levels of detail.
    - Ignore any difference in style, grammar, or punctuation.
    
    The allowed categories can be either of: Spoofing, Tampering, Repudiation, Information Disclosure,
    Denial of Service, Elevation of Privilege.
    The allowed assets are: {assets}.
    
    Some examples of threats that are similar are:
    |                    Threat A                     |                   Threat B                     |
    |-------------------------------------------------|------------------------------------------------|
    | Attackers may exploit improperly implemented    | A malicious user performs an SQL injection     |
    | input validation mechanisms, and thereby gain   | and they gain unauthorized access to the       |
    | unauthorized access to the system               | system                                         |
    |-------------------------------------------------|------------------------------------------------|
    | An attacker manages to elevate their privileges | A user gains access to an admin account        |
    |-------------------------------------------------|------------------------------------------------|
    | The system is flooded with requests,            | An attacker performs a Denial of Service       |
    | overwhelming system resources and rendering it  | attack on the system                           |
    | unresponsive                                    |                                                |
    |-------------------------------------------------|------------------------------------------------|
    
    You should only consider the fields: Category, Asset, and Threat in the dictionary elements in the two lists.
    
    The two lists are:
    [List 1]
    {tm1}
    
    [List 2]
    {tm2}
    
    Please return the IDs of the elements that are similar as a list of tuples (ID1, ID2).
    
    Once you have completed the task, please end your response with this JSON object:
    {{
        "same": [("ID1", "ID2"),...]
    }}
"""

MITIGATION_PROMPT = """
    You are an impartial judge, and you will be comparing the elements in the tuples stored in a lists.
    You are provided with a lists of tuples, and you need to find out if the elements in a tuple
    are similar based on the following criteria:
    - The mitigations suggest one or more of the same method(s).
    - Not all suggested mitigations need to be present in both, a subset is allowed.
    - The mitigations may be worded differently, use abbrevations, or have different levels of detail.
    - Ignore any difference in style, grammar, or punctuation.
    
    Some examples of mitigations that suggest the same method(s) are:
    |                  Mitigation A                   |                Mitigation B                    |
    |-------------------------------------------------|------------------------------------------------|
    | Implement strict input validation on all        | Sanitize user input before applying it         |
    | user-supplied data to prevent injection         | anywhere in the system, and use an allowlist   |
    | attacks like SQL and XSS                        | if possible                                    |
    |-------------------------------------------------|------------------------------------------------|
    | Restrict access rights using the principle of   | Implement a mechanism that ensures that a user |
    | least privilege                                 | only has the capabilities they actually need   |
    |-------------------------------------------------|------------------------------------------------|
    | Enforce MFA for all users to prevent            | Use multi-factor authentication                |
    | unauthorized access to possibly sensitive data. |                                                |
    |-------------------------------------------------|------------------------------------------------|
    
    You should only consider the field: Mitigation in the dictionary elements in the tuples.
    
    The list to analyze is:
    [List]
    {tm}
    
    Please return the tuples which adhere with the criteria in a list.
    
    Once you have completed the task, please end your response with this JSON object:
    {{
        "same": [("ID1", "ID2"),...]
    }}
"""

RISK_PROMPT = """
    You are an impartial judge, and you will be comparing the elements in the tuples stored in a lists.
    You are provided with a lists of tuples, and you need to find out if the elements in a tuple
    are similar based on the following criteria:
    - The risk present the same level of severity irregardless of the format.
    - Ignore any difference in style, grammar, or punctuation.
    
    Some examples of risks that present the same level of severity are:
    |   Risk A    |    Risk B     |
    |-------------|---------------|
    | High Risk   | 3 out of 3    |
    |-------------|---------------|
    | Medium Risk | 50 out of 100 |
    |-------------|---------------|
    | Low Risk    | 3 out of 10   |
    |-------------|---------------|
    
    Some examples of risks where Risk B is lower than Risk A:
    |   Risk A    |    Risk B     |
    |-------------|---------------|
    | High Risk   | 2 out of 3    |
    |-------------|---------------|
    | Medium Risk | 10 out of 100 |
    |-------------|---------------|
    | Low Risk    | 2 out of 10   |
    |-------------|---------------|

    Some examples of risks where Risk B is higher than Risk A:
    |   Risk A    |    Risk B     |
    |-------------|---------------|
    | Medium Risk | 79 out of 100 |
    |-------------|---------------|
    | Low Risk    | 8 out of 10   |
    |-------------|---------------|
    | Low Risk    | 5 out of 10   |
    |-------------|---------------|
    
    You should only consider the field: Risk in the dictionary elements in the tuples.
    
    The list to analyze is:
    [List]
    {tm}
    
    Please return three lists, one with the tuples where the risk is the same, 
    one where the risk in the first tuple element is higher than the second element,
    and on where the risk in the first tuple element is lower than the second element.
    
    Once you have completed the task, please end your response with this JSON object:
    {{
        "same": [("ID1", "ID2"),...],
        "more": [("ID1", "ID2"),...]
        "less": [("ID1", "ID2"),...]
    }}
"""