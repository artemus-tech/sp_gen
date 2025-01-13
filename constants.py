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