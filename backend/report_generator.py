def generate_report(diagnosis):
    # In a real application, this would be more sophisticated
    report = f"""
    Medical Report
    --------------
    Diagnosis: Class ID {diagnosis}

    Recommendations:
    - Further analysis is recommended.
    - Consult a specialist for detailed evaluation.
    """
    return report
