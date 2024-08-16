def find_value(table, *keys):
    for key in keys:
        if isinstance(table, dict):
            # Attempt to find the key directly
            if key in table:
                table = table[key]
            else:
                # If the key is not found, check for comma-separated keys
                found = False
                for k in table.keys():
                    if key in k.split(', '):
                        table = table[k]
                        found = True
                        break
                if not found:
                    raise KeyError(f"Key '{key}' not found in the table.")
        else:
            raise ValueError("Reached a non-dictionary structure in the table.")
    return table

# Function to check Value
def check_value(val, allowableVal):
    if allowableVal is None:
        return "Value limit not found"
    
    val = int(val)
    allowableVal = int(allowableVal)
    
    if val <= allowableVal:
        return "Passed"
    else:
        return "Failed"