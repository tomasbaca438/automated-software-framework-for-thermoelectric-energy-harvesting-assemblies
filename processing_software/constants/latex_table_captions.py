from constants.csv_columns import CSVColumns


class LatexTableCaptions:

    CAPTIONS = {

        f"{CSVColumns.TEMPERATURE_HOT_COLUMN}_static_properties":
            "Static properties of the heat spreader temperature [°C] for different load resistances.",

        f"{CSVColumns.TEMPERATURE_COLD_COLUMN}_static_properties":
            "Static properties of the cooling structure temperature [°C] for different load resistances.",

        f"{CSVColumns.TEMPERATURE_DIFFERENCE_COLUMN}_static_properties":
            "Static properties of the temperature difference [°C] for different load resistances.",

        f"{CSVColumns.CURRENT_COLUMN}_static_properties":
            "Static properties of the output current [mA] for different load resistances.",

        f"{CSVColumns.VOLTAGE_COLUMN}_static_properties":
            "Static properties of the output voltage [V] for different load resistances.",

        f"{CSVColumns.POWER_COLUMN}_static_properties":
            "Static properties of the output power [mW] for different load resistances.",

        f"{CSVColumns.SEEBECK_COEFFICIENT_COLUMN}_static_properties":
            "Static properties of the Seebeck coefficient [mV/°C] for different load resistances.",

        f"{CSVColumns.TEMPERATURE_HOT_COLUMN}_rising_dynamic_properties":
            "Rising dynamic properties of the heat spreader temperature [°C].",

        f"{CSVColumns.TEMPERATURE_HOT_COLUMN}_falling_dynamic_properties":
            "Falling dynamic properties of the heat spreader temperature [°C].",

        f"{CSVColumns.TEMPERATURE_COLD_COLUMN}_rising_dynamic_properties":
            "Rising dynamic properties of the cooling structure temperature [°C].",

        f"{CSVColumns.TEMPERATURE_COLD_COLUMN}_falling_dynamic_properties":
            "Falling dynamic properties of the cooling structure temperature [°C].",

        f"{CSVColumns.TEMPERATURE_DIFFERENCE_COLUMN}_rising_dynamic_properties":
            "Rising dynamic properties of the temperature difference [°C].",

        f"{CSVColumns.TEMPERATURE_DIFFERENCE_COLUMN}_falling_dynamic_properties":
            "Falling dynamic properties of the temperature difference [°C].",

        f"{CSVColumns.CURRENT_COLUMN}_rising_dynamic_properties":
            "Rising dynamic properties of the output current [mA].",

        f"{CSVColumns.CURRENT_COLUMN}_falling_dynamic_properties":
            "Falling dynamic properties of the output current [mA].",

        f"{CSVColumns.VOLTAGE_COLUMN}_rising_dynamic_properties":
            "Rising dynamic properties of the output voltage [V].",

        f"{CSVColumns.VOLTAGE_COLUMN}_falling_dynamic_properties":
            "Falling dynamic properties of the output voltage [V].",

        f"{CSVColumns.POWER_COLUMN}_rising_dynamic_properties":
            "Rising dynamic properties of the output power [mW].",

        f"{CSVColumns.POWER_COLUMN}_falling_dynamic_properties":
            "Falling dynamic properties of the output power [mW].",

        f"{CSVColumns.SEEBECK_COEFFICIENT_COLUMN}_rising_dynamic_properties":
            "Rising dynamic properties of the Seebeck coefficient [mV/°C].",

        f"{CSVColumns.SEEBECK_COEFFICIENT_COLUMN}_falling_dynamic_properties":
            "Falling dynamic properties of the Seebeck coefficient [mV/°C].",

        f"{CSVColumns.TEMPERATURE_HOT_COLUMN}_rising_first_order_validation":
            "Validation of the first-order approximation for the rising heat spreader temperature response [°C].",

        f"{CSVColumns.TEMPERATURE_HOT_COLUMN}_falling_first_order_validation":
        "Validation of the first-order approximation for the falling heat spreader temperature response [°C].",

        f"{CSVColumns.TEMPERATURE_COLD_COLUMN}_rising_first_order_validation":
        "Validation of the first-order approximation for the rising cooling structure temperature response [°C].",

        f"{CSVColumns.TEMPERATURE_COLD_COLUMN}_falling_first_order_validation":
        "Validation of the first-order approximation for the falling cooling structure temperature response [°C].",

        f"{CSVColumns.TEMPERATURE_DIFFERENCE_COLUMN}_rising_first_order_validation":
        "Validation of the first-order approximation for the rising temperature-difference response [°C].",

        f"{CSVColumns.TEMPERATURE_DIFFERENCE_COLUMN}_falling_first_order_validation":
        "Validation of the first-order approximation for the falling temperature-difference response [°C].",

        f"{CSVColumns.CURRENT_COLUMN}_rising_first_order_validation":
        "Validation of the first-order approximation for the rising output-current response [mA].",

        f"{CSVColumns.CURRENT_COLUMN}_falling_first_order_validation":
        "Validation of the first-order approximation for the falling output-current response [mA].",

        f"{CSVColumns.VOLTAGE_COLUMN}_rising_first_order_validation":
        "Validation of the first-order approximation for the rising output-voltage response [V].",

        f"{CSVColumns.VOLTAGE_COLUMN}_falling_first_order_validation":
        "Validation of the first-order approximation for the falling output-voltage response [V].",

        f"{CSVColumns.POWER_COLUMN}_rising_first_order_validation":
        "Validation of the first-order approximation for the rising output-power response [mW].",

        f"{CSVColumns.POWER_COLUMN}_falling_first_order_validation":
        "Validation of the first-order approximation for the falling output-power response [mW].",

        f"{CSVColumns.SEEBECK_COEFFICIENT_COLUMN}_rising_first_order_validation":
        "Validation of the first-order approximation for the rising apparent Seebeck-coefficient response [mV/°C].",

        f"{CSVColumns.SEEBECK_COEFFICIENT_COLUMN}_falling_first_order_validation":
        "Validation of the first-order approximation for the falling apparent Seebeck-coefficient response [mV/°C].",

        f"{CSVColumns.TEMPERATURE_HOT_COLUMN}_rising_nls_dynamic_properties":
            "Rising dynamic properties of the heat spreader temperature [°C] determined using nonlinear least-squares fitting.",

        f"{CSVColumns.TEMPERATURE_HOT_COLUMN}_falling_nls_dynamic_properties":
            "Falling dynamic properties of the heat spreader temperature [°C] determined using nonlinear least-squares fitting.",

        f"{CSVColumns.TEMPERATURE_COLD_COLUMN}_rising_nls_dynamic_properties":
            "Rising dynamic properties of the cooling structure temperature [°C] determined using nonlinear least-squares fitting.",

        f"{CSVColumns.TEMPERATURE_COLD_COLUMN}_falling_nls_dynamic_properties":
            "Falling dynamic properties of the cooling structure temperature [°C] determined using nonlinear least-squares fitting.",

        f"{CSVColumns.TEMPERATURE_DIFFERENCE_COLUMN}_rising_nls_dynamic_properties":
            "Rising dynamic properties of the temperature difference [°C] determined using nonlinear least-squares fitting.",

        f"{CSVColumns.TEMPERATURE_DIFFERENCE_COLUMN}_falling_nls_dynamic_properties":
            "Falling dynamic properties of the temperature difference [°C] determined using nonlinear least-squares fitting.",

        f"{CSVColumns.CURRENT_COLUMN}_rising_nls_dynamic_properties":
            "Rising dynamic properties of the output current [mA] determined using nonlinear least-squares fitting.",

        f"{CSVColumns.CURRENT_COLUMN}_falling_nls_dynamic_properties":
            "Falling dynamic properties of the output current [mA] determined using nonlinear least-squares fitting.",

        f"{CSVColumns.VOLTAGE_COLUMN}_rising_nls_dynamic_properties":
            "Rising dynamic properties of the output voltage [V] determined using nonlinear least-squares fitting.",

        f"{CSVColumns.VOLTAGE_COLUMN}_falling_nls_dynamic_properties":
            "Falling dynamic properties of the output voltage [V] determined using nonlinear least-squares fitting.",

        f"{CSVColumns.POWER_COLUMN}_rising_nls_dynamic_properties":
            "Rising dynamic properties of the output power [mW] determined using nonlinear least-squares fitting.",

        f"{CSVColumns.POWER_COLUMN}_falling_nls_dynamic_properties":
            "Falling dynamic properties of the output power [mW] determined using nonlinear least-squares fitting.",

        f"{CSVColumns.SEEBECK_COEFFICIENT_COLUMN}_rising_nls_dynamic_properties":
            "Rising dynamic properties of the Seebeck coefficient [mV/°C] determined using nonlinear least-squares fitting.",

        f"{CSVColumns.SEEBECK_COEFFICIENT_COLUMN}_falling_nls_dynamic_properties":
            "Falling dynamic properties of the Seebeck coefficient [mV/°C] determined using nonlinear least-squares fitting.",

        "rising_tau_correlation_matrix":
            (
                "Pearson correlation matrix of the rising "
                "time constants obtained using the "
                "crossing-based estimator."
            ),

        "falling_tau_correlation_matrix":
            (
                "Pearson correlation matrix of the falling "
                "time constants obtained using the "
                "crossing-based estimator."
            ),

        "rising_nls_tau_correlation_matrix":
            (
                "Pearson correlation matrix of the rising "
                "time constants obtained using nonlinear "
                "least-squares fitting."
            ),

        "falling_nls_tau_correlation_matrix":
            (
                "Pearson correlation matrix of the falling "
                "time constants obtained using nonlinear "
                "least-squares fitting."
            ),
    }