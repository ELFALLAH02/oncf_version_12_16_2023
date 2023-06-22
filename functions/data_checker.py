valid_x = None

# Define a function named 'checker' that takes three parameters: 'min_date', 'max_date', and 'df'
def checker(min_date, max_date, df):
    # Declare 'valid_x' as a global variable
    global valid_x
    
    # Initialize 'start_checker' and 'end_checker' variables as None
    start_checker = None
    end_checker = None
    
    # Loop through the 'new_date' column in the 'df' DataFrame
    for i in df['new_date']:
        # Check if the current value matches the 'min_date'
        if i == min_date:
            # Set 'start_checker' to 'valid_start' if a match is found
            start_checker = 'valid_start'
            break
        else:
            # Set 'start_checker' to 'invalid_start' if no match is found
            start_checker = 'invalid_start'
    
    # Loop through the 'new_date' column in the 'df' DataFrame
    for x in df['new_date']:
        # Check if the current value matches the 'max_date'
        if x == max_date:
            # Set 'end_checker' to 'valid_end' if a match is found
            end_checker = 'valid_end'
            break
        else:
            # Set 'end_checker' to 'invalid_end' if no match is found
            end_checker = 'invalid_end'
    
    # Check the conditions to determine the validity of the date range
    if (start_checker == 'valid_start') and (end_checker == 'valid_end'):
        return True
    elif (start_checker == 'valid_start') and (end_checker == 'invalid_end'):
        valid_x = 'end_checker_inv'
        return valid_x
    elif (start_checker == 'invalid_start') and (end_checker == 'valid_end'):
        valid_x = 'start_checker_inv'
        return valid_x
    elif (start_checker == 'invalid_start') and (end_checker == 'invalid_end'):
        valid_x = 'both invalid'
        return valid_x
