import numpy as np
import pandas as pd
from constants.csv_columns import CSVColumns
import os

class CSVMerger:

    @classmethod
    def __interpolate_voltage_current_dataset(
            cls,
            df_temp: pd.DataFrame,
            df_vc: pd.DataFrame) -> pd.DataFrame:
        source_index = np.linspace(0, len(df_vc) - 1, len(df_vc))
        target_index = np.linspace(0, len(df_vc) - 1, len(df_temp))
        df_vc_sync = pd.DataFrame()
        df_vc_sync[CSVColumns.CURRENT_COLUMN] = np.interp(
            target_index, source_index, df_vc[CSVColumns.CURRENT_COLUMN])
        df_vc_sync[CSVColumns.VOLTAGE_COLUMN] = np.interp(
            target_index, source_index, df_vc[CSVColumns.VOLTAGE_COLUMN])
        return df_vc_sync

    @classmethod
    def merge_datasets(
            cls,
            temperature_file_paths: list[str],
            voltage_current_file_paths: list[str],
            merged_file_paths: list[str]) -> None:
        for temp_path, vc_path, merged_path in zip(
                temperature_file_paths, voltage_current_file_paths, merged_file_paths):
            df_temp = pd.read_csv(temp_path, sep=";")
            df_vc = pd.read_csv(vc_path, sep=";")
            df_vc_sync = cls.__interpolate_voltage_current_dataset(
                df_temp, df_vc)
            df_merged = pd.DataFrame()
            df_merged[CSVColumns.SAMPLE_COLUMN] = df_temp[CSVColumns.SAMPLE_COLUMN]
            df_merged[CSVColumns.TEMPERATURE_HOT_COLUMN] = df_temp[CSVColumns.TEMPERATURE_HOT_COLUMN]
            df_merged[CSVColumns.TEMPERATURE_COLD_COLUMN] = df_temp[CSVColumns.TEMPERATURE_COLD_COLUMN]
            df_merged[CSVColumns.CURRENT_COLUMN] = df_vc_sync[CSVColumns.CURRENT_COLUMN]
            df_merged[CSVColumns.VOLTAGE_COLUMN] = df_vc_sync[CSVColumns.VOLTAGE_COLUMN]
            df_merged[CSVColumns.TEMPERATURE_DIFFERENCE_COLUMN] = (
                df_merged[CSVColumns.TEMPERATURE_HOT_COLUMN] - df_merged[CSVColumns.TEMPERATURE_COLD_COLUMN])
            df_merged[CSVColumns.POWER_COLUMN] = (
                df_merged[CSVColumns.VOLTAGE_COLUMN] * df_merged[CSVColumns.CURRENT_COLUMN])
            df_merged[CSVColumns.SEEBECK_COEFFICIENT_COLUMN] = np.where(
                df_merged[CSVColumns.TEMPERATURE_DIFFERENCE_COLUMN] == 0,
                0,
                1000 * df_merged[CSVColumns.VOLTAGE_COLUMN] / df_merged[CSVColumns.TEMPERATURE_DIFFERENCE_COLUMN])
            os.makedirs(
                os.path.dirname(merged_path),
                exist_ok=True
            )
            df_merged.to_csv(merged_path, sep=";", index=False)
            print(f"Merged file saved: {merged_path}")