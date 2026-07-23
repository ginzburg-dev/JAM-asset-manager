"""Statistics API placeholders for the JAM community edition."""


def _commercial_feature(*_args, **_kwargs):
    raise NotImplementedError("Statistics are available only in the commercial edition.")


def calculate_efficiency(start_date, end_date, format, data_types):
    return _commercial_feature(start_date, end_date, format, data_types)


def compare_data(first_dataset, second_dataset, start_date, end_date, format, data_types):
    return _commercial_feature(
        first_dataset, second_dataset, start_date, end_date, format, data_types
    )


def calculate_AI_prediction(start_date, end_date, data_types):
    return _commercial_feature(start_date, end_date, data_types)


def get_raw_statistics(start_date, end_date, data_types):
    return _commercial_feature(start_date, end_date, data_types)


def export_statistics_to_XML(data, format, data_types):
    return _commercial_feature(data, format, data_types)
