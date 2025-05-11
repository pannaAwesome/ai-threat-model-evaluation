
SYSTEM_PROMPT = """
    You are an impartial judge, and you will be comparing the elements of two lists.
    Each list represents a threat model, and you will need to determine, which elements are similar based on 
    a user specified criteria. You should eek to find single best match, and you cannot match one elements
    in one list with multiple elements in the other.
    
    You should always ignore any difference in style, grammar, or punctuation.
    
    Each element for comparison is a dictionary with the following keys:
    - ID: The ID of the threat.
    - Category: The category of the threat.
    - Threat: A description of the threat itself.
    - Mitigation: A description of the mitigation for the threat.
    - Risk: The risk of the threat, this can either be one of: High Severity, Medium Severity, Low Severity, 
            or a numerical value written as '<score> out of <max>'.
    - (Optional) Asset: The asset that the threat targets.
    If the list directly contains dictionaries, you need to compare one element from each list,
    whereas if the list contains tuples of dictionaries, you need to compare the first element in the tuple
    with the second element in the tuple.
    
    The categories can be either of: Spoofing, Tampering, Repudiation, Information Disclosure,
    Denial of Service, Elevation of Privilege.
    The assets can be either of: {assets}.
"""

HALLUCINATIONS_PROMPT = """
    You need to discover if any of the elements of the list use different categories or assets than what is expected.
    You have previously been told which categories we allow, and which assets are used in the application.
    
    The category can be verified purely from looking at the 'Category' field in the dictionary.
    The assets should be verified in two ways:
    1. The 'Asset' field if present
    2. The 'Threat' field, the description will detail some assets in the system, commonly these are capitalized
       and they will be either cause of the threat or be impacted by it.
    
    Some examples of assets in a threat description are:
        
    The list is:
    [List]
    {tm}
    
    Please return (ID,category) of the elements that have different categories than expected in category_list,
    and (ID,[assets]) of the elements that have different assets than expected in asset_list. If no elements are
    found then return empty lists.
    
    Once you have completed the task, please end your response with this JSON object:
    {{
        "category_list": [("ID", category),...],
        "asset_list": [("ID", [assets]),...]
    }}
"""

THREAT_PROMPT = """
    You need to discover the elements in the two lists that are similar based on the following criteria:
    - The category of the threats are the same.
    - If asset is specified for both threats, then they should be the same. Otherwise,
      you can defer the asset based on the threat description, the asset would be the entry point
      of the attack.
    - The threats have the same malicious objective and impact, the impact might not be explicitly stated
      in the threat description, but it can be inferred from the context.
    - The threats may be worded differently, use abbreviations or have different levels of detail.
    
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
    | overwhelming system resources and rendering it  | attck on the system                            |
    | unresponsive                                    |                                                |
    |-------------------------------------------------|------------------------------------------------|
    
    You should only consider the fields: Category, Asset, and Threat in the dictionary elements in the two lists.
    
    The two lists are:
    [List 1]
    {tm1}
    
    [List 2]
    {tm2}
    
    Please return the IDs of the elements that are similar as a list of tuples (ID1, ID2),
    a list of elements only present in List1, and a list of elements only present in List2.
    
    Once you have completed the task, please end your response with this JSON object:
    {{
        "similar_threats": [("ID1", "ID2"),...],
        "list1_only": ["ID1",...],
        "list2_only": ["ID2",...]
    }}
"""

MITIGATION_PROMPT = """
    You are provided with two lists of tuples, and you need to find out if the elements in a tuple
    are similar based on the following criteria:
    - The mitigations suggest the same method(s)
    - The mitigations may be worded differently, use abbrevations, or have different levels of detail.
    
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
    
    The two lists are:
    [List 1]
    {tm1}
    
    [List 2]
    {tm2}
    
    Please return the IDs of the elements that are similar as a list of tuples (ID1, ID2),
    a list of elements only present in List1, and a list of elements only present in List2.
    
    Once you have completed the task, please end your response with this JSON object:
    {{
        "similar_threats": [("ID1", "ID2"),...],
        "list1_only": ["ID1",...],
        "list2_only": ["ID2",...]
    }}
"""

RISK_PROMPT = """
    You are provided with two lists of tuples, and you need to find out if the elements in a tuple
    are similar based on the following criteria:
    - The risk present the same level of severity irregardless of the format.
    
    Some examples of risks that present the same level of severity are:
    |   Risk A    |    Risk B     |
    |-------------|---------------|
    | High Risk   | 3 out of 3    |
    |-------------|---------------|
    | Medium Risk | 50 out of 100 |
    |-------------|---------------|
    | Low Risk    | 3 out of 10   |
    |-------------|---------------|
    
    You should only consider the field: Risk in the dictionary elements in the tuples.
    
    The two lists are:
    [List 1]
    {tm1}
    
    [List 2]
    {tm2}
    
    Please return the IDs of the elements that are similar as a list of tuples (ID1, ID2),
    a list of elements only present in List1, and a list of elements only present in List2.
    
    Once you have completed the task, please end your response with this JSON object:
    {{
        "similar_threats": [("ID1", "ID2"),...],
        "list1_only": ["ID1",...],
        "list2_only": ["ID2",...]
    }}
"""