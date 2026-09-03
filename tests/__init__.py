def without_provenance(response):
    """Remove separately tested build metadata from numerical golden responses."""
    if isinstance(response, list):
        return [without_provenance(measurement) for measurement in response]
    return {key: value for key, value in response.items() if key != "provenance"}
