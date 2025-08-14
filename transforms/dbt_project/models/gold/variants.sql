##Minimal dbt models (gold)
{{ config(materialized='table') }}

with base as (
  select
    -- in real pipeline: select from silver tables
    1 as patient_key,
    'SAMPLE_001' as sample_id,
    'GRCh38' as build,
    '17' as chrom,
    7673803 as pos,
    'C' as ref,
    'T' as alt,
    'TP53' as gene,
    'missense_variant' as consequence,
    'p.R175H' as hgvs_p,
    'Pathogenic' as clin_sig,
    current_timestamp as load_ts
)
select * from base
