import psycopg2


tables = [
    "eval_results",
    "generate_results",
    "model_mean_intensity",
    "proxima_intensity",
    "vrija_results",
    "integral_results"
]


tables_dict = {
    "eval":"eval_results",
    "gen":"generate_results",
    "mean_eval":"model_mean_intensity",
    "proxima":"proxima_intensity",
    "vrija":"vrija_results",
    "integral_intensity":"integral_results"
}
try_count=10 ** 12


current_path = 'C:\\sp_gen\\legacy\\data'

active_table_dict={
    "sp_gen":"sp_gen",
    "sp_eval":"sp_eval",
    "sp_intens":"sp_intens",
    "sp_mono":"sp_mono",
    "sp_dec":"sp_dec",
    "sp_res":"sp_res",
    "sp_vrija":"sp_vrija",
    "sp_gen_legacy":"generate_results",
    "sp_eval_legacy":"eval_results"

}
path_speval = 'C:\sp_gen\legacy\data'
path_intensity_sum_norm_avg='C:\sp_gen\legacy\data\sp_intensity_sum_norm_avg'
path_avg  = "C:\sp_gen\legacy\data\sp_avg_eval"
path_trapezoid_vrija ="C:\sp_gen\legacy\data\sp_vrija_trapezoid"
path_integral  = "C:\sp_gen\legacy\data\sp_intensity_integral"
path_vrija ="C:\sp_gen\legacy\data\sp_vrija_no_volume_complex"
path_to_lm_dec="C:\sp_gen\legacy\data\sp_lm_dec_intensity"
path_to_dump="C:\sp_gen\legacy\data\sp_dump"
