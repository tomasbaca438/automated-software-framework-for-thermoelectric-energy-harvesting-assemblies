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
            "Falling dynamic properties of the Seebeck coefficient [mV/°C]."
    }