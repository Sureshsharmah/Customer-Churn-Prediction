import pandas as pd
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metrics import DatasetDriftMetric

def check_drift(current_data, reference_data):
    column_mapping = ColumnMapping(
        target=None,
        numerical_features=['tenure', 'MonthlyCharges', 'TotalCharges'],
        categorical_features=['Contract', 'InternetService']
    )
    
    report = Report(metrics=[DatasetDriftMetric()])
    report.run(
        current_data=current_data,
        reference_data=reference_data,
        column_mapping=column_mapping
    )
    return report.as_dict()