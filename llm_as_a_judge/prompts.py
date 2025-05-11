
SYSTEM_PROMPT = """
    You are an impartial judge, and you will be comparing the elements of two lists.
    Each list represents a threat model, and you will need to determine, which elements are similar based on 
    a user specified criteria. You should always ignore any differences in style, grammar, or punctuation.
    
    The lists are in a JSON format, and each element in the list is a dictionary with the following keys:
    - ID: The ID of the threat.
    - Category: The category of the threat.
    - Threat: A description of the threat itself.
    - Mitigation: A description of the mitigation for the threat.
    - Risk: The risk of the threat, this can either be one of: High Severity, Medium Severity, Low Severity, 
            or a numerical value written as '<score> out of <max>'.
    - (Optional) Asset: The asset that the threat targets.
    
    The categories can be either of: Spoofing, Tampering, Repudiation, Information Disclosure,
    Denial of Service, Elevation of Privilege.
    The assets can be either of: {assets}.
"""

THREAT_PROMPT = {
    "message": """
        You need to discover the elements in the two lists that are similar based on the following criteria:
        - The category of the threats are the same.
        - If asset is specified in both lists, then they should be the same.
        - The threats have the same malicious objective and impact.
        You should only consider the fields: Category, Asset, and Threat of the JSON objects in the lists.
        
        The two lists are:
        [List 1]
        {tm1}
        
        [List 2]
        {tm2}
        
        Return the IDs of the elements that are similar as a list of tuples (ID1, ID2),
        a list of elements only present in List1, and a list of elements only present in List2.
    """,
    "name": "find_similar_threats",
    "description": """
        Return the IDs of the elements that are similar as a list of tuples (ID1, ID2),
        a list of elements only present in List1, and a list of elements only present in List2
    """,
    "output_lists": ["similar_threats", "list1_only", "list2_only"]
}

