# main.py
import pandas as pd
from sympy import symbols
from sympy.logic.boolalg import SOPform, POSform
import re

def solve_boolean_expression(expression_str, variables):
    """
    Solves a boolean expression string (in minterm or maxterm format)
    to find its SOP and POS forms.

    Args:
        expression_str (str): The string from the CSV, e.g., "Σ m[4, 5, 8, 12, 13]".
        variables (list): A list of sympy symbols, e.g., [A, B, C, D].

    Returns:
        tuple: A tuple containing the SOP and POS expression strings.
               Returns (None, None) if the format is invalid.
    """
    # Determine the total number of possible values based on variable count (e.g., 4 vars -> 2^4=16)
    num_vars = len(variables)
    all_values = set(range(2**num_vars))

    # Use regex to find all numbers within brackets []
    try:
        terms = [int(t) for t in re.findall(r'\d+', expression_str)]
    except (ValueError, TypeError):
        return None, None # Return None if parsing fails

    sop_expression = None
    pos_expression = None

    # Check if the expression is in Sum of Products (minterms) format
    if 'm' in expression_str or 'Σ' in expression_str:
        minterms = terms
        # Maxterms are all the values not present in minterms
        maxterms = list(all_values - set(minterms))
        
        # Ensure minterms are not empty before calculating
        if minterms:
            sop_expression = SOPform(variables, minterms)
        # Ensure maxterms are not empty before calculating
        if maxterms:
            pos_expression = POSform(variables, maxterms)

    # Check if the expression is in Product of Sums (maxterms) format
    elif 'M' in expression_str or 'Π' in expression_str:
        maxterms = terms
        # Minterms are all the values not present in maxterms
        minterms = list(all_values - set(maxterms))

        # Ensure minterms are not empty before calculating
        if minterms:
            sop_expression = SOPform(variables, minterms)
        # Ensure maxterms are not empty before calculating
        if maxterms:
            pos_expression = POSform(variables, maxterms)
            
    else:
        # If the format is not recognized
        return "Invalid Format", "Invalid Format"

    return str(sop_expression), str(pos_expression)

def main():
    """
    Main function to read the CSV, process expressions, and print the results.
    """
    # --- Configuration ---
    # Define the variables for the boolean expressions.
    # The problems use numbers up to 15, which implies 4 variables.
    A, B, C, D = symbols('A, B, C, D')
    variables = [A, B, C, D]
    
    # Specify the name of your input CSV file
    input_csv_filename = 'problems.csv'
    # Specify the name for the output CSV file
    output_csv_filename = 'solved_expressions.csv'

    try:
        # Read the CSV file using pandas
        df = pd.read_csv(input_csv_filename)
    except FileNotFoundError:
        print(f"Error: The file '{input_csv_filename}' was not found.")
        print("Please make sure the CSV file is in the same directory as the script.")
        return

    # Prepare lists to store the results
    sop_results = []
    pos_results = []

    # Get the name of the first column, which contains the expressions
    expression_column_name = df.columns[0]

    # Iterate over each expression in the first column
    for expression in df[expression_column_name]:
        # Ensure the expression is a string before processing
        if isinstance(expression, str):
            sop, pos = solve_boolean_expression(expression, variables)
            sop_results.append(sop)
            pos_results.append(pos)
        else:
            # Handle empty or non-string rows
            sop_results.append('')
            pos_results.append('')

    # Add the results as new columns to the DataFrame
    df['SOP'] = sop_results
    df['POS'] = pos_results

    # Save the updated DataFrame to a new CSV file
    df.to_csv(output_csv_filename, index=False)

    print(f"Processing complete. The results have been saved to '{output_csv_filename}'")
    # Optional: print the results to the console
    print("\n--- Results ---")
    print(df.to_string())

if __name__ == '__main__':
    main()
