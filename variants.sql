-- models/gold/variants.sql
{{ config(materialized='delta') }}

with base as (
  select
    p.patient_key,
    v.sample_id,
    v.build,
    v.chrom, v.pos, v.ref, v.alt,
    a.gene, a.consequence, a.hgvs_p, a.hgvs_c,
    a.clin_sig, a.oncogenicity, a.tumor_suppressor_flag,
    current_timestamp() as load_ts
  from silver.variants v
  join silver.variant_annotations a
    on v.variant_id = a.variant_id
  join silver.sample_patient_link spl
    on v.sample_id = spl.sample_id
  join gold.patient p
    on spl.patient_uid = p.patient_uid
)
select * from base;
